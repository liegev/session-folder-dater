# session-folder-dater

Prefix each Pro Tools or Ableton session folder with the date of its oldest file.

Session folders get copied, renamed and backed up until nobody remembers when the
music was made. The oldest audio file inside is the best record of that date.

```
Bass idea          ->  2019-07-14 Bass idea
Chorus rework v3   ->  2021-03-02 Chorus rework v3
```

## Use

```sh
python3 session_folder_dater.py /Volumes/MUSIC/staging          # dry run: shows what would change
python3 session_folder_dater.py /Volumes/MUSIC/staging --apply  # renames
```

- Works on every folder directly inside the path you give it.
- Folders that already start with a date are left alone.
- Uses the file creation date where the OS keeps one (macOS, Windows) and the
  modification date elsewhere.
- Skips `.DS_Store`, `._*` and other OS clutter.

No dependencies beyond Python 3.
