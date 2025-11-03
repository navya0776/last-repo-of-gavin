using Microsoft.Win32;
using OfficeOpenXml;
using OfficeOpenXml.Style;
using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using Excel = Microsoft.Office.Interop.Excel;

namespace IMS.Views
{
    public partial class AnalysisAP : Page
    {
        public AnalysisAP()
        {
            InitializeComponent();
            LoadMockData();
        }

        private void LedgerDataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
        }


        //private void Export_Click(object sender, RoutedEventArgs e)
        //{
        //    // Auto detect visible column headers
        //    var allFields = LedgerDataGrid.Columns
        //        .Select(c => c.Header.ToString())
        //        .ToList();

        //    Windows.FieldSelectionWindow dialog = new Windows.FieldSelectionWindow(allFields);
        //    dialog.Owner = Window.GetWindow(this);

        //    if (dialog.ShowDialog() == true && dialog.SelectedFields.Any())
        //        ExportToExcel(dialog.SelectedFields);
        //}

 

        private void LoadMockData()
        {
            var mockData = new List<StockItem>()
            {
                new StockItem
                {
                    PageNo = 12, ScaleNo = "S-23", PartNo = "PN-4567", Nomen = "Hydraulic Pump Assembly",
                    AU = "EA", Auth = 20, CurrStck = 15, DuesIn = 5, OutsReqd = 2, StkN = 18, ReqdOHS = 22,
                    Ptrn = 3, ReqdCons = 25, QtyDem = 8, Received = 4, DepotCtrl = "Yes", DepCtrlDt = "14-Jan-2025",
                    SubDemNo = "SDN-0023"
                },
                new StockItem
                {
                    PageNo = 14, ScaleNo = "S-55", PartNo = "PN-8921", Nomen = "Fuel Filter Cartridge",
                    AU = "EA", Auth = 50, CurrStck = 30, DuesIn = 10, OutsReqd = 5, StkN = 35, ReqdOHS = 40,
                    Ptrn = 6, ReqdCons = 45, QtyDem = 12, Received = 8, DepotCtrl = "No", DepCtrlDt = "-",
                    SubDemNo = "SDN-0098"
                }
            };

            LedgerDataGrid.ItemsSource = mockData;
        }
    }

    public class StockItem
    {
        public int PageNo { get; set; }
        public string ScaleNo { get; set; }
        public string PartNo { get; set; }
        public string Nomen { get; set; }
        public string AU { get; set; }
        public int Auth { get; set; }
        public int CurrStck { get; set; }
        public int DuesIn { get; set; }
        public int OutsReqd { get; set; }
        public int StkN { get; set; }
        public int ReqdOHS { get; set; }
        public int Ptrn { get; set; }
        public int ReqdCons { get; set; }
        public int QtyDem { get; set; }
        public int Received { get; set; }
        public string DepotCtrl { get; set; }
        public string DepCtrlDt { get; set; }
        public string SubDemNo { get; set; }
    }
}
