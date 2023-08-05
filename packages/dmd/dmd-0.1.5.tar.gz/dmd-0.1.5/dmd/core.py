import fnmatch
import glob
import logging
import os
from time import sleep
from typing import TextIO, Iterator, Tuple, Collection

import jinja2
import markdown as md
from watchdog import observers, events

from .extensions import CoreExtension


class DndMarkdown:
    def __init__(self, template: jinja2.Template) -> None:
        self._template = template

    def convert(self, output_file: TextIO, markdown_file: TextIO) -> None:
        Converter(self._template).convert(markdown_file, output_file)

    def convert_all(self, md_root: str, html_root: str) -> None:
        MultiConverter(Converter(self._template), FileManager(md_root, html_root)).convert_all()

    def watch(self, md_root: str, html_root: str) -> None:
        Observer(Converter(self._template), md_root, html_root).watch()

    def set_template(self, template: jinja2.Template):
        self._template = template


class FileChangeResult:
    def __init__(self, created_files: Collection[str] = None, removed_files: Collection[str] = None,
                 updated_files: Collection[str] = None, created_dirs: Collection[str] = None,
                 removed_dirs: Collection[str] = None) -> None:
        self._created_files = set(created_files if created_files is not None else [])
        self._removed_files = set(removed_files if removed_files is not None else [])
        self._updated_files = set(updated_files if updated_files is not None else [])
        self._created_dirs = set(created_dirs if created_dirs is not None else [])
        self._removed_dirs = set(removed_dirs if removed_dirs is not None else [])

    def __add__(self, other: 'FileChangeResult') -> 'FileChangeResult':
        return FileChangeResult(
            created_files=self._created_files.union(other._created_files),
            removed_files=self._removed_files.union(other._removed_files),
            updated_files=self._updated_files.union(other._updated_files),
            created_dirs=self._created_dirs.union(other._created_dirs),
            removed_dirs=self._removed_dirs.union(other._removed_dirs)
        )._resolve()

    def __iter__(self) -> Iterator[Tuple[str, int, str]]:
        if len(self._removed_files) > 0:
            yield 'removed', len(self._removed_files), 'files'
        if len(self._removed_dirs) > 0:
            yield 'removed', len(self._removed_dirs), 'dirs'
        if len(self._created_dirs) > 0:
            yield 'created', len(self._created_dirs), 'dirs'
        if len(self._created_files) > 0:
            yield 'created', len(self._created_files), 'files'
        if len(self._updated_files) > 0:
            yield 'updated', len(self._updated_files), 'files'

    def _resolve(self) -> 'FileChangeResult':
        self._updated_files.update(self._created_files.intersection(self._removed_files))
        self._created_files.difference_update(self._updated_files)
        self._removed_files.difference_update(self._updated_files)
        updated_dirs = self._created_dirs.intersection(self._removed_dirs)
        self._created_dirs.difference_update(updated_dirs)
        self._removed_dirs.difference_update(updated_dirs)
        return self


class CreatedFile(FileChangeResult):
    def __init__(self, path: str) -> None:
        super().__init__(created_files=[path])


class RemovedFile(FileChangeResult):
    def __init__(self, path: str) -> None:
        super().__init__(removed_files=[path])


class UpdatedFile(FileChangeResult):
    def __init__(self, path: str) -> None:
        super().__init__(updated_files=[path])


class CreatedDir(FileChangeResult):
    def __init__(self, path: str) -> None:
        super().__init__(created_dirs=[path])


class RemovedDir(FileChangeResult):
    def __init__(self, path: str) -> None:
        super().__init__(removed_dirs=[path])


class FileManager:
    def __init__(self, md_root: str, html_root: str) -> None:
        super().__init__()
        self._md_root = os.path.abspath(md_root)
        self._html_root = os.path.abspath(html_root)

        self._md_glob_pattern = os.path.join(self._md_root, '**/*.md')
        self._html_glob_pattern = os.path.join(self._html_root, '**/*.html')
        self._assets_glob_pattern = os.path.join(self._html_root, 'assets/**/*')

        self._md_fnmatch_pattern = os.path.join(self._md_root, '*.md')
        self._html_fnmatch_pattern = os.path.join(self._html_root, '*.html')

    def get_all_md_paths(self) -> list:
        paths = glob.glob(self._md_glob_pattern, recursive=True)
        return sorted([os.path.abspath(path) for path in paths])

    def get_all_html_paths(self) -> list:
        paths = set(glob.glob(self._html_glob_pattern, recursive=True))
        paths.difference_update(glob.glob(self._assets_glob_pattern, recursive=True))
        return sorted([os.path.abspath(path) for path in paths])

    def get_html_path_from_md_path(self, md_path: str) -> str:
        md_dir, md_base = os.path.split(md_path)
        rel_dir = os.path.relpath(md_dir, self._md_root)
        html_base = md_base[:-3] + '.html'
        html_path = os.path.join(self._html_root, rel_dir, html_base)

        return os.path.normpath(html_path)

    def make_directory_and_ancestors(self, path: str, is_file: bool = True) -> FileChangeResult:
        if os.path.exists(path):
            return FileChangeResult()

        result = self.make_directory_and_ancestors(os.path.dirname(path), False)
        if not is_file:
            os.mkdir(path)
            logging.debug('Created %s', path)
            result += CreatedDir(path)
        return result

    def is_md(self, path: str, must_exist: bool = True) -> bool:
        path = os.path.abspath(path)
        return fnmatch.fnmatch(path, self._md_fnmatch_pattern) and (not must_exist or os.path.isfile(path))

    def is_html(self, path: str, must_exist: bool = True) -> bool:
        path = os.path.abspath(path)
        return fnmatch.fnmatch(path, self._html_fnmatch_pattern) and (not must_exist or os.path.isfile(path))

    def remove_html(self, path) -> FileChangeResult:
        if not self.is_html(path):
            raise ValueError
        os.remove(path)
        logging.debug('Deleted %s', path)
        return RemovedFile(path)

    def remove_all_html(self) -> FileChangeResult:
        result = FileChangeResult()
        for html_path in self.get_all_html_paths():
            result += self.remove_html(html_path)
            result += self.remove_empty_in_html_path(html_path)
        return result

    def remove_empty_in_html_path(self, path: str) -> FileChangeResult:
        if os.path.commonprefix([path, self._html_root]) != self._html_root:
            raise ValueError
        result = FileChangeResult()
        if os.path.exists(path):
            try:
                os.rmdir(path)
                logging.debug('Deleted %s', path)
                result += RemovedDir(path)
            except (NotADirectoryError, OSError):
                return result
        try:
            result += self.remove_empty_in_html_path(os.path.dirname(path))
        except ValueError:
            pass
        return result


class Converter:
    def __init__(self, template: jinja2.Template) -> None:
        super().__init__()
        self._md = md.Markdown(extensions=[
            CoreExtension(),
            'tables',
            'extra',
        ])
        self._template = template

    def convert(self, in_: TextIO, out: TextIO) -> None:
        in_str = ''
        while True:
            line = in_.readline()
            if not line:
                break
            in_str += line
        out_str = self._md.convert(in_str) + '\n'

        out.write(self._template.render(body=out_str))


class MultiConverter:
    def __init__(self, converter: Converter, file_manager: FileManager) -> None:
        self._converter = converter
        self._manager = file_manager

    def convert_all(self) -> None:
        result = self._manager.remove_all_html()
        for md_path in self._manager.get_all_md_paths():
            html_path = self._manager.get_html_path_from_md_path(md_path)
            result += self._manager.make_directory_and_ancestors(html_path)
            with open(md_path, 'r') as md_file, open(html_path, 'w+') as html_file:
                self._converter.convert(md_file, html_file)
                logging.debug('Created %s', html_path)
                result += CreatedFile(html_path)
        for operation, num, type_ in result:
            logging.info('%s %d %s', operation.capitalize(), num, type_)


class Observer(events.FileSystemEventHandler):
    def __init__(self, converter: Converter, md_root: str, html_root: str) -> None:
        super().__init__()
        self._converter = converter
        self._manager = FileManager(md_root, html_root)
        self._observer = observers.Observer()
        self._md_root = md_root

    def watch(self) -> None:
        self._observer.schedule(self, self._md_root, recursive=True)
        self._observer.start()
        try:
            while True:
                sleep(1)
        except KeyboardInterrupt:
            self._observer.stop()
        self._observer.join()

    def on_moved(self, event: events.FileSystemMovedEvent) -> None:
        if event.is_directory \
                or not self._manager.is_md(event.src_path, False) \
                or not self._manager.is_md(event.dest_path):
            return

        html_old_path = self._manager.get_html_path_from_md_path(event.src_path)
        self._remove_if_exists(html_old_path)
        self._manager.remove_empty_in_html_path(html_old_path)

        html_new_path = self._manager.get_html_path_from_md_path(event.dest_path)
        self._manager.make_directory_and_ancestors(html_new_path)
        self._convert(event.dest_path, html_new_path)

    def on_created(self, event: events.FileCreatedEvent) -> None:
        if event.is_directory or not self._manager.is_md(event.src_path):
            return

        html_path = self._manager.get_html_path_from_md_path(event.src_path)
        self._manager.make_directory_and_ancestors(html_path)
        self._convert(event.src_path, html_path)

    def on_deleted(self, event: events.FileDeletedEvent) -> None:
        if event.is_directory or not self._manager.is_md(event.src_path):
            return

        html_path = self._manager.get_html_path_from_md_path(event.src_path)
        self._remove_if_exists(html_path)
        self._manager.remove_empty_in_html_path(html_path)

    def on_modified(self, event: events.FileModifiedEvent) -> None:
        if event.is_directory or not self._manager.is_md(event.src_path):
            return

        html_path = self._manager.get_html_path_from_md_path(event.src_path)
        self._convert(event.src_path, html_path)

    def _remove_if_exists(self, path: str) -> None:
        try:
            self._manager.remove_html(path)
        except ValueError:
            pass

    def _convert(self, in_path: str, out_path: str) -> None:
        operation = 'Updated' if self._manager.is_html(out_path) else 'Created'
        with open(in_path, 'r') as in_file, open(out_path, 'w+') as out_file:
            self._converter.convert(in_file, out_file)
            logging.debug('%s %s', operation, out_path)
