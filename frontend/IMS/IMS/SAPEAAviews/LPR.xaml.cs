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
    public partial class LPR : Page
    {
        public class LPRItem
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

        public ObservableCollection<LPRItem> LPRList { get; set; }

        private List<LPRItem> _fullBackupList;
        private List<string> _columns;

        public LPR()
        {
            InitializeComponent();

            LPRList = new ObservableCollection<LPRItem>();
            DataContext = this;

            LoadLPRItems();
        }

        // -----------------------------------------------------------
        // LOAD LPR DATA
        // -----------------------------------------------------------
        private async void LoadLPRItems()
        {
            //try
            //{
            //    var list = await ApiService.GetLPRListAsync();

            //    LPRList.Clear();
            //    foreach (var item in list)
            //        LPRList.Add(item);

            //    _fullBackupList = list.ToList();

            //    LoadColumnSelector();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Failed to load LPR data.\n" + ex.Message,
            //                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            //}
        }

        // -----------------------------------------------------------
        // COLUMN SELECTOR FOR SEARCH
        // -----------------------------------------------------------
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

        // -----------------------------------------------------------
        // SEARCH FILTER
        // -----------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_fullBackupList == null) return;

            string column = ColumnSelector.SelectedItem?.ToString();
            string keyword = SearchBox.Text.Trim().ToLower();

            if (string.IsNullOrWhiteSpace(keyword))
            {
                ResetList();
                return;
            }

            var filtered = _fullBackupList.Where(v =>
            {
                var value = v.GetType().GetProperty(column)?.GetValue(v, null);
                return value != null && value.ToString().ToLower().Contains(keyword);
            });

            LPRList.Clear();
            foreach (var item in filtered)
                LPRList.Add(item);
        }

        private void ResetList()
        {
            LPRList.Clear();
            foreach (var item in _fullBackupList)
                LPRList.Add(item);
        }

        // -----------------------------------------------------------
        // DATE FILTER (Last X days)
        // -----------------------------------------------------------
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
                ResetList();
                return;
            }

            var threshold = DateTime.Now.AddDays(-days);

            var filtered = _fullBackupList.Where(v => v.Date >= threshold);

            LPRList.Clear();
            foreach (var item in filtered)
                LPRList.Add(item);
        }

        // -----------------------------------------------------------
        // HEADER BACK BUTTON
        // -----------------------------------------------------------
        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }

        // -----------------------------------------------------------
        // FOOTER BUTTONS (Placeholders)
        // -----------------------------------------------------------
        private void Print_DOS_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("DOS Print not implemented.");
        }

        private void Print_Win_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Windows Print not implemented.");
        }

        private void Print_Word_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Word Export not implemented.");
        }

        private void Print_Preview_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Print Preview not implemented.");
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
