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
    public partial class InspNote : Page
    {
        public ObservableCollection<ChallanItem> InspList { get; set; }

        private List<ChallanItem> _fullBackupList;
        private List<string> _columns;

        public InspNote()
        {
            InitializeComponent();

            InspList = new ObservableCollection<ChallanItem>();
            DataContext = InspList;

            LoadData();
        }

        // ---------------------------------------------------------------
        // LOAD DATA FROM BACKEND
        // ---------------------------------------------------------------
        private async void LoadData()
        {
            //try
            //{
            //    // Replace this call with your actual API
            //    var data = await ApiService.GetInspectionNoteAsync();

            //    InspList.Clear();
            //    foreach (var item in data)
            //        InspList.Add(item);

            //    _fullBackupList = data.ToList();

            //    LoadColumnSelector();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Failed to load Inspection Note data:\n" + ex.Message,
            //                    "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            //}
        }

        // ---------------------------------------------------------------
        // POPULATE COLUMN SELECTOR
        // ---------------------------------------------------------------
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

        // ---------------------------------------------------------------
        // SEARCH BOX FILTER
        // ---------------------------------------------------------------
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_fullBackupList == null) return;

            string keyword = SearchBox.Text.Trim().ToLower();
            string column = ColumnSelector.SelectedItem?.ToString();

            if (string.IsNullOrWhiteSpace(keyword))
            {
                ResetList();
                return;
            }

            var filtered = _fullBackupList.Where(v =>
            {
                var prop = v.GetType().GetProperty(column)?.GetValue(v, null);
                if (prop == null) return false;
                return prop.ToString().ToLower().Contains(keyword);
            });

            InspList.Clear();
            foreach (var item in filtered)
                InspList.Add(item);
        }

        private void ResetList()
        {
            InspList.Clear();
            foreach (var item in _fullBackupList)
                InspList.Add(item);
        }

        // ---------------------------------------------------------------
        // DAYS FILTER
        // ---------------------------------------------------------------
        private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (_fullBackupList == null) return;

            string selection = (DaysFilterBox.SelectedItem as ComboBoxItem)?.Content.ToString();

            int days = selection switch
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

            DateTime threshold = DateTime.Now.AddDays(-days);

            var filtered = _fullBackupList.Where(v => v.Date >= threshold);

            InspList.Clear();
            foreach (var item in filtered)
                InspList.Add(item);
        }

        // ---------------------------------------------------------------
        // BACK BUTTON
        // ---------------------------------------------------------------
        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }

        // ---------------------------------------------------------------
        // FOOTER BUTTONS (PLACEHOLDERS)
        // ---------------------------------------------------------------
        private void Print_DOS_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("DOS Print Coming Soon!");
        }

        private void Print_Win_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Windows Print Coming Soon!");
        }

        private void Print_Word_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Word Export Coming Soon!");
        }

        private void Print_Preview_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Print Preview Coming Soon!");
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
