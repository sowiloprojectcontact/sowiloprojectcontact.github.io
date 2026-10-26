#!/usr/bin/env python3
"""Package only public website files for GitHub Pages, never the workspace."""
from pathlib import Path
import hashlib
import zipfile
from check_site import check

ROOT=Path(__file__).resolve().parents[1]


def public_files():
    files=list(ROOT.glob('*.html'))+[ROOT/'style.css',ROOT/'robots.txt',ROOT/'.nojekyll']
    for folder in ('articles','assets'):
        files.extend(path for path in (ROOT/folder).rglob('*') if path.is_file())
    for path in files:
        if path.is_symlink() or not path.resolve().is_relative_to(ROOT):raise ValueError('Unsafe public source')
        if path.suffix.lower() not in ('.html','.css','.svg','.png','.jpg','.jpeg','.webp','.ico','.txt') and path.name!='.nojekyll':raise ValueError('Unexpected public file: '+str(path))
    return sorted(set(files))


def package():
    count=check(ROOT)
    destination=ROOT/'dist';destination.mkdir(exist_ok=True)
    target=destination/'sowilo-github-pages.zip'
    with zipfile.ZipFile(target,'w',compression=zipfile.ZIP_DEFLATED) as archive:
        for path in public_files():archive.write(path,path.relative_to(ROOT).as_posix())
    checksum=hashlib.sha256(target.read_bytes()).hexdigest()
    target.with_suffix('.zip.sha256').write_text(checksum+'  '+target.name+'\n')
    print(f'{count} pages validated; public archive: {target}')
    return target


if __name__=='__main__':package()
