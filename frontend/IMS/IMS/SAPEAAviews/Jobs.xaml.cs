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
    public partial class Jobs : Page
    {
        public ObservableCollection<ChallanItem> JobList { get; set; }

        private List<ChallanItem> _backupList;
        private List<string> _columns;

        public Jobs()
        {
            InitializeComponent();

            JobList = new ObservableCollection<ChallanItem>();
            DataContext = JobList;

            LoadData();
        }

        // --------------------------------------------------------
        // LOAD DATA FROM API
        // --------------------------------------------------------
        private async void LoadData()
        {
            //try
            //{
            //    var data = await ApiService.GetJobsAsync(); // <<< your API method

            //    JobList.Clear();
            //    foreach (var d in data)
            //        JobList.Add(d);

            //    _backupList = data.ToList();

            //    LoadColumnSelector();
            //}
            //catch (Exception ex)
            //{
            //    MessageBox.Show("Failed to load Job Details:\n" + ex.Message,
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
                "Status",
                "Job_No_Comp_Dt"
            };

            ColumnSelector.ItemsSource = _columns;
            ColumnSelector.SelectedIndex = 0;
        }

        // --------------------------------------------------------
        // SEARCH FUNCTION
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

            JobList.Clear();
            foreach (var f in filtered)
                JobList.Add(f);
        }

        private void ResetList()
        {
            JobList.Clear();
            foreach (var item in _backupList)
                JobList.Add(item);
        }

        // --------------------------------------------------------
        // LAST X DAYS FILTER
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

            JobList.Clear();
            foreach (var item in filtered)
                JobList.Add(item);
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
            MessageBox.Show("DOS Print not implemented yet.");
        }

        private void Print_Win_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Windows Print not implemented yet.");
        }

        private void Print_Word_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Word export not implemented yet.");
        }

        private void Print_Preview_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Print preview not implemented yet.");
        }

        private void Close_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
