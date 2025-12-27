using System;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using OfficeOpenXml;
using Microsoft.Win32;
using System.IO;

namespace IMS.Views
{
    public partial class JobMaster : Page
    {
        private readonly string _eqptCode;

        private ObservableCollection<LedgerMockItem> _fullList =
            new ObservableCollection<LedgerMockItem>();

        public ObservableCollection<LedgerMockItem> JobList { get; set; } =
            new ObservableCollection<LedgerMockItem>();

        private int _currentPage = 1;
        private readonly int _pageSize = 25;

        public JobMaster(string eqptCode)
        {
            _eqptCode = eqptCode;
            InitializeComponent();
            DataContext = this;

            LoadMockData();   // USING MOCK DATA
        }

        // --------------------------------------------------------------------
        // MOCK DATA LOADER (Matches EXACTLY your DataGrid columns)
        // --------------------------------------------------------------------
        private void LoadMockData()
        {
            _fullList.Clear();

            Random R = new Random();

            for (int i = 1; i <= 50; i++)
            {
                _fullList.Add(new LedgerMockItem
                {
                    idx = i,
                    ledger_page = "LP-" + (1000 + i),
                    ohs_number = "OHS-" + (2000 + i),
                    isg_number = "ISG-" + (3000 + i),
                    ssg_number = "SSG-" + (4000 + i),

                    part_number = "PART-" + i,
                    nomenclature = "Component Item " + i,
                    a_u = R.Next(1, 5).ToString(),

                    no_off = R.Next(1, 20),
                    scl_auth = "AUTH-" + i,

                    unsv_stock = R.Next(0, 50),
                    rep_stock = R.Next(0, 30),
                    serv_stock = R.Next(0, 40),

                    msc = "MSC-" + (i % 4),
                    ved = "VED-" + (i % 3),
                    in_house = (i % 2 == 0) ? "Yes" : "No",

                    bin_number = "BIN-" + i,
                    group = "G-" + (i % 10),

                    cds_unsv_stock = R.Next(0, 20),
                    cds_rep_stock = R.Next(0, 20),
                    cds_serv_stock = R.Next(0, 20),

                    lpp = 1000 + R.Next(0, 500),
                    rate = 20 + R.Next(0, 10),

                    rmks = "Remarks for item " + i,
                    lpp_dt = DateTime.Now.AddDays(-i).ToString("dd-MM-yyyy")
                });
            }

            ApplyPaging();

            ActiveEquipmentList.Items.Clear();
            ActiveEquipmentList.Items.Add(_eqptCode);
        }

        // --------------------------------------------------------------------
        // SEARCH FUNCTION
        // --------------------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            string search = SearchTextBox.Text.Trim().ToLower();

            if (string.IsNullOrEmpty(search))
            {
                ApplyPaging();
                return;
            }

            var filtered = _fullList.Where(x =>
                    x.part_number.ToLower().Contains(search) ||
                    x.nomenclature.ToLower().Contains(search) ||
                    x.ohs_number.ToLower().Contains(search) ||
                    x.isg_number.ToLower().Contains(search) ||
                    x.ssg_number.ToLower().Contains(search)
                ).ToList();

            JobList.Clear();
            foreach (var item in filtered)
                JobList.Add(item);
        }

        // --------------------------------------------------------------------
        // PAGINATION
        // --------------------------------------------------------------------
        private void Prev_Click(object sender, RoutedEventArgs e)
        {
            if (_currentPage > 1)
            {
                _currentPage--;
                ApplyPaging();
            }
        }

        private void Next_Click(object sender, RoutedEventArgs e)
        {
            _currentPage++;
            ApplyPaging();
        }

        private void ApplyPaging()
        {
            JobList.Clear();

            var items = _fullList
                        .Skip((_currentPage - 1) * _pageSize)
                        .Take(_pageSize);

            foreach (var item in items)
                JobList.Add(item);
        }



        private void ExportExcel_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                ExcelPackage.LicenseContext = LicenseContext.NonCommercial;

                SaveFileDialog saveDialog = new SaveFileDialog
                {
                    Filter = "Excel Files (*.xlsx)|*.xlsx",
                    FileName = "JobMasterData.xlsx"
                };

                if (saveDialog.ShowDialog() != true)
                    return;

                using (ExcelPackage package = new ExcelPackage())
                {
                    var ws = package.Workbook.Worksheets.Add("JobMaster");

                    string[] headers =
                    {
                "Index", "Ledger Page", "OHS No", "ISG No", "SSG No",
                "Part No", "Nomenclature", "A/U", "No Off", "Scl Auth",
                "Unsv Stock", "Rep Stock", "Serv Stock",
                "MSC", "VED", "In-House", "Bin No", "Group",
                "CDS Unsv", "CDS Rep", "CDS Serv",
                "LPP", "Rate", "Remarks", "LPP Date"
            };

                    // Write header
                    for (int i = 0; i < headers.Length; i++)
                        ws.Cells[1, i + 1].Value = headers[i];

                    // Write rows
                    int row = 2;
                    foreach (var item in JobList)
                    {
                        ws.Cells[row, 1].Value = item.idx;
                        ws.Cells[row, 2].Value = item.ledger_page;
                        ws.Cells[row, 3].Value = item.ohs_number;
                        ws.Cells[row, 4].Value = item.isg_number;
                        ws.Cells[row, 5].Value = item.ssg_number;

                        ws.Cells[row, 6].Value = item.part_number;
                        ws.Cells[row, 7].Value = item.nomenclature;
                        ws.Cells[row, 8].Value = item.a_u;
                        ws.Cells[row, 9].Value = item.no_off;
                        ws.Cells[row, 10].Value = item.scl_auth;

                        ws.Cells[row, 11].Value = item.unsv_stock;
                        ws.Cells[row, 12].Value = item.rep_stock;
                        ws.Cells[row, 13].Value = item.serv_stock;

                        ws.Cells[row, 14].Value = item.msc;
                        ws.Cells[row, 15].Value = item.ved;
                        ws.Cells[row, 16].Value = item.in_house;

                        ws.Cells[row, 17].Value = item.bin_number;
                        ws.Cells[row, 18].Value = item.group;

                        ws.Cells[row, 19].Value = item.cds_unsv_stock;
                        ws.Cells[row, 20].Value = item.cds_rep_stock;
                        ws.Cells[row, 21].Value = item.cds_serv_stock;

                        ws.Cells[row, 22].Value = item.lpp;
                        ws.Cells[row, 23].Value = item.rate;

                        ws.Cells[row, 24].Value = item.rmks;
                        ws.Cells[row, 25].Value = item.lpp_dt;

                        row++;
                    }

                    ws.Cells.AutoFitColumns();

                    FileInfo excelFile = new FileInfo(saveDialog.FileName);
                    package.SaveAs(excelFile);
                }

                MessageBox.Show("Exported Successfully!", "Excel", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Excel Export Failed\n{ex.Message}");
            }
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService?.GoBack();
        }


        // ------------------------------------------------------------------------
        // MODEL CLASS MATCHING YOUR DATAGRID COLUMNS EXACTLY
        // ------------------------------------------------------------------------
        public class LedgerMockItem
        {
            public int idx { get; set; }
            public string ledger_page { get; set; }
            public string ohs_number { get; set; }
            public string isg_number { get; set; }
            public string ssg_number { get; set; }

            public string part_number { get; set; }
            public string nomenclature { get; set; }
            public string a_u { get; set; }

            public int no_off { get; set; }
            public string scl_auth { get; set; }

            public int unsv_stock { get; set; }
            public int rep_stock { get; set; }
            public int serv_stock { get; set; }

            public string msc { get; set; }
            public string ved { get; set; }
            public string in_house { get; set; }

            public string bin_number { get; set; }
            public string group { get; set; }

            public int cds_unsv_stock { get; set; }
            public int cds_rep_stock { get; set; }
            public int cds_serv_stock { get; set; }

            public int lpp { get; set; }
            public int rate { get; set; }

            public string rmks { get; set; }
            public string lpp_dt { get; set; }
        }
    }
}

