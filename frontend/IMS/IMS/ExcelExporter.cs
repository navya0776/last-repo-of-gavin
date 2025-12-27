using ClosedXML.Excel;
using IMS.Models;
using System.Collections.Generic;
using System.Data;
using System.Reflection;

namespace IMS.Helpers
{
    public static class ExcelExporter
    {
        public static void Export<T>(List<T> data, string filePath)
        {
            using (var workbook = new XLWorkbook())
            {
                var dataTable = ToDataTable(data);
                workbook.Worksheets.Add(dataTable, "Export");
                workbook.SaveAs(filePath);
            }
        }

        internal static void Export(string fileName, IEnumerable<LedgerItem> items, List<string> selectedHeaders, List<object> propNames)
        {
            using (var workbook = new XLWorkbook())
            {
                var ws = workbook.Worksheets.Add("Ledger Export");

                // ---------------------------
                // Write headers
                // ---------------------------
                for (int i = 0; i < selectedHeaders.Count; i++)
                {
                    ws.Cell(1, i + 1).Value = selectedHeaders[i];
                    ws.Cell(1, i + 1).Style.Font.Bold = true;
                    ws.Cell(1, i + 1).Style.Fill.BackgroundColor = XLColor.LightGray;
                }

                // ---------------------------
                // Write row data
                // ---------------------------
                int row = 2;
                foreach (var item in items)
                {
                    for (int col = 0; col < propNames.Count; col++)
                    {
                        string propName = propNames[col].ToString();
                        var prop = item.GetType().GetProperty(propName);

                        if (prop != null)
                        {
                            var value = prop.GetValue(item);
                            ws.Cell(row, col + 1).Value = value?.ToString() ?? "";
                        }
                    }

                    row++;
                }

                ws.Columns().AdjustToContents();
                workbook.SaveAs(fileName);
            }
        }


        private static DataTable ToDataTable<T>(List<T> items)
        {
            DataTable table = new DataTable(typeof(T).Name);

            PropertyInfo[] properties = typeof(T).GetProperties();
            foreach (PropertyInfo prop in properties)
                table.Columns.Add(prop.Name);

            foreach (var item in items)
            {
                var values = new object[properties.Length];
                for (int i = 0; i < properties.Length; i++)
                    values[i] = properties[i].GetValue(item);

                table.Rows.Add(values);
            }

            return table;
        }
    }
}
