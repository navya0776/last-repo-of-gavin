using Microsoft.Reporting.WinForms;
using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace IMS.Reports
{
    internal class ReportForm
    {
        private void ReportForm_Load(object sender, EventArgs e)
        {
            DataTable dt = new DataTable("DataSet1");

            dt.Columns.Add("SrlNo", typeof(string));
            dt.Columns.Add("OSNo", typeof(string));
            dt.Columns.Add("PartNo", typeof(string));
            dt.Columns.Add("Nomenclature", typeof(string));
            dt.Columns.Add("AU", typeof(string));
            dt.Columns.Add("ScaleAuth", typeof(string));
            dt.Columns.Add("NoOff", typeof(string));
            dt.Columns.Add("Cat", typeof(string));

            // If grouping is needed:
            dt.Columns.Add("GroupName", typeof(string));

            // Fill rows here from your database...
            // dt.Rows.Add("1", "OS23", "P-10", "GEAR", "A", "10", "5", "M", "GROUP A");

            ReportDataSource rds = new ReportDataSource("DataSet1", dt);

            reportViewer1.LocalReport.DataSources.Clear();
            reportViewer1.LocalReport.DataSources.Add(rds);
            reportViewer1.RefreshReport();
        }

    }
}
