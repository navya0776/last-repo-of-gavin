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
            throw new NotImplementedException();
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
