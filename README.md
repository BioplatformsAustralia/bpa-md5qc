# Quick MD5 file QC

Verify that, for each MD5 file passed through on as an argument:

 - that all files in the MD5 file exist (does *not* verify the checksum)
 - that there are no other files in the same directory which are not contained in the file, or in another MD5 file in the same directory (also passed through as an argument for checking)

Intended for use on a flat-file archive.

Usage:

```
/mnt/Q0185/marine_microbes/raw$ find . -name "*.md5" -print  | xargs bpa-md5qc
```


