using IMS.Models;
using IMS.Services;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using static IMS.SAPEAAviews.Challan;

namespace IMS.SAPEAAviews
{
    public partial class Item : Page
    {
        public ObservableCollection<ChallanItem> ItemList { get; set; }

        private List<ChallanItem> _backupList;
        private List<string> _columns;

        public Item()
        {
            InitializeComponent();

            ItemList = new ObservableCollection<ChallanItem>();
            DataContext = ItemList;

            LoadData();
        }

        // --------------------------------------------------------
        // LOAD DATA FROM API
        // --------------------------------------------------------
        private async void LoadData()
        {
            //try
            //{
            //    var data = await ApiService.GetItemDataAsync(); // Change to your real API

            //    ItemList.Clear();
            //    foreach (var d in data)
            //        ItemList.Add(d);

            //    _backupList = data.ToList();

            //    LoadColumnSelector();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Failed to load Item data:\n" + ex.Message,
            //                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            //}
        }

        // --------------------------------------------------------
        // POPULATE COLUMN DROPDOWN
        // --------------------------------------------------------
        private void LoadColumnSelector()
        {
            _columns = new List<string>
            {
                "Lpr_No",
                "Indent_No",
                "Part_No",
                "Nomen",
                "Vend",
                "Status"
            };

            ColumnSelector.ItemsSource = _columns;
            ColumnSelector.SelectedIndex = 0;
        }

        // --------------------------------------------------------
        // SEARCH TEXT CHANGED
        // --------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_backupList == null) return;

            string keyword = SearchBox.Text.Trim().ToLower();
            string column = ColumnSelector.SelectedItem?.ToString();

            if (string.IsNullOrWhiteSpace(keyword))
            {
                ResetList();
                return;
            }

            var filtered = _backupList.Where(row =>
            {
                var property = row.GetType().GetProperty(column)?.GetValue(row, null);
                if (property == null) return false;
                return property.ToString().ToLower().Contains(keyword);
            });

            ItemList.Clear();
            foreach (var f in filtered)
                ItemList.Add(f);
        }

        private void ResetList()
        {
            ItemList.Clear();
            foreach (var item in _backupList)
                ItemList.Add(item);
        }

        // --------------------------------------------------------
        // DAYS FILTER (7, 15, 30, 90)
        // --------------------------------------------------------
        private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (_backupList == null) return;

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

            DateTime cutoff = DateTime.Now.AddDays(-days);

            var filtered = _backupList.Where(row => row.Date >= cutoff);

            ItemList.Clear();
            foreach (var item in filtered)
                ItemList.Add(item);
        }

        // --------------------------------------------------------
        // BACK BUTTON
        // --------------------------------------------------------
        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }

        // --------------------------------------------------------
        // FOOTER BUTTONS
        // --------------------------------------------------------
        private void Print_DOS_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Feature not implemented yet.");
        }

        private void Print_Win_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Feature not implemented yet.");
        }

        private void Print_Word_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Feature not implemented yet.");
        }

        private void Print_Preview_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Feature not implemented yet.");
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
