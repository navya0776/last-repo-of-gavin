using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace IMS.SAPEAAviews
{
    public partial class Vendor : Page
    {

        public class VendorItem
        {
            public int Srl { get; set; }
            public string Lpr_No { get; set; }
            public DateTime Date { get; set; }
            public string Indent_No { get; set; }
            public string Job_No_Comp_Dt { get; set; }
            public string Ohs { get; set; }
            public string Page { get; set; }
            public string Part_No { get; set; }
            public string Nomen { get; set; }
            public int Qty { get; set; }
            public int Recd { get; set; }
            public string So { get; set; }
            public DateTime So_Date { get; set; }
            public string Vend { get; set; }
            public decimal Rate { get; set; }
            public string Status { get; set; }
        }

        public ObservableCollection<VendorItem> VendorList { get; set; }
        private List<VendorItem> _fullBackupList;   // For filtering
        private List<string> _columns;              // For searching

        public Vendor()
        {
            InitializeComponent();

            VendorList = new ObservableCollection<VendorItem>();
            DataContext = this;

            LoadVendors();
        }

        // ------------------------------------------------------
        //  LOAD VENDOR DATA
        // ------------------------------------------------------
        private async void LoadVendors()
        {
            //try
            //{
            //    // CALL YOUR API
            //    var list = await ApiService.GetVendorListAsync();
            //    // You MUST create this inside ApiService

            //    VendorList.Clear();
            //    foreach (var item in list)
            //        VendorList.Add(item);

            //    // Backup for search filtering
            //    _fullBackupList = list.ToList();

            //    LoadColumnSelector();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Error loading Vendor data:\n" + ex.Message);
            //}
        }

        // ------------------------------------------------------
        //  POPULATE COLUMN DROPDOWN FOR SEARCHING
        // ------------------------------------------------------
        private void LoadColumnSelector()
        {
            _columns = new List<string>
            {
                "Lpr_No",
                "Indent_No",
                "Job_No_Comp_Dt",
                "Part_No",
                "Nomen",
                "Vend",
                "Status"
            };

            ColumnSelector.ItemsSource = _columns;
            ColumnSelector.SelectedIndex = 0;
        }

        // ------------------------------------------------------
        //  SEARCH BOX FILTERING
        // ------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_fullBackupList == null) return;

            string keyword = SearchBox.Text.Trim().ToLower();
            string column = ColumnSelector.SelectedItem?.ToString();

            if (string.IsNullOrWhiteSpace(keyword))
            {
                // Reset
                VendorList.Clear();
                foreach (var v in _fullBackupList)
                    VendorList.Add(v);
                return;
            }

            var filtered = _fullBackupList.Where(v =>
            {
                var prop = v.GetType().GetProperty(column)?.GetValue(v, null);
                if (prop == null) return false;
                return prop.ToString().ToLower().Contains(keyword);
            });

            VendorList.Clear();
            foreach (var x in filtered)
                VendorList.Add(x);
        }

        // ------------------------------------------------------
        //  LAST X DAYS FILTER
        // ------------------------------------------------------
        private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (_fullBackupList == null) return;

            string selected = (DaysFilterBox.SelectedItem as ComboBoxItem)?.Content.ToString();

            int days = selected switch
            {
                "Last 7 Days" => 7,
                "Last 15 Days" => 15,
                "Last 30 Days" => 30,
                "Last 90 Days" => 90,
                _ => 0
            };

            if (days == 0)
            {
                VendorList.Clear();
                foreach (var v in _fullBackupList)
                    VendorList.Add(v);
                return;
            }

            var threshold = DateTime.Now.AddDays(-days);

            var filtered = _fullBackupList.Where(v => v.Date >= threshold);

            VendorList.Clear();
            foreach (var v in filtered)
                VendorList.Add(v);
        }

        // ------------------------------------------------------
        //  BACK BUTTON
        // ------------------------------------------------------
        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }

        // ------------------------------------------------------
        //  FOOTER BUTTON PLACEHOLDERS
        // ------------------------------------------------------
        private void Print_DOS_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("DOS Printing not yet implemented.");
        }

        private void Print_Win_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Windows Printing not yet implemented.");
        }

        private void Print_Word_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Word Export not implemented yet.");
        }

        private void Print_Preview_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Printer Preview not implemented.");
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
