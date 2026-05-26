# Critical Text Collation - Validations

## No Spaces in Collation Cells

### **Id**
collate-no-spaces-in-cells
### **Severity**
error
### **Type**
regex
### **Pattern**
  - (?i)cell_value.*?\s+.*?
### **Message**
Collation cell contains a raw space character; spaces within cells must be replaced by the bullet character '•' to represent multiple-entity nodes
### **Fix Action**
Replace raw spaces with the bullet character (U+2022) in the cell string formatting.

---

## Segment Column Missing

### **Id**
collate-segment-column-missing
### **Severity**
error
### **Type**
regex
### **Pattern**
  - ^(?!.*segment).*$
### **Message**
Excel sheet is missing the required 'segment' column in Column A
### **Fix Action**
Ensure the output workbook writes 'segment' in the first cell (A1) and uses Column A for sentence group indexes.

---

## Strikethrough Formatting Mappings

### **Id**
collate-invalid-strikethrough
### **Severity**
warning
### **Type**
regex
### **Pattern**
  - <(?!del|strike|s\b)[^>]*\\.*?>
### **Message**
Canceled text run within an interpolation lacks correct strikethrough formatting in the spreadsheet representation
### **Fix Action**
Map all prior text before backslashes (e.g., `<prior\interpolated>`) to use the strikethrough font property in Excel.
