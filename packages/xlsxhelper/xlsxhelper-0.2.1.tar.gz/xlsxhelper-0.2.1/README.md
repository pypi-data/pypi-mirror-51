# xlsxhelper

Excel file manipulation toolset. 


## Notice

The library is based on library openpyxl, so only xlsx (new excel format) files are supported.

## Help Functions

- get_workbook
- get_worksheet
- get_merged_range_string
- parse_cols
- parse_rows
- get_cells
- load_data_from_workbook
- get_merged_ranges
- copy_cells
- merge_ranges


## Release Note


### v0.2.1

- Fix load_data_from_workbook get raw function statement problem.
- Fix worksheet.merged_cell_ranges deprecating problem, use worksheet.merged_cells.ranges instead.
