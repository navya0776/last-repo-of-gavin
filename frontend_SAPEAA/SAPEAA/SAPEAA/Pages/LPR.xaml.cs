using IMS.Models;
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
        private ObservableCollection<LPRItem> _allItems = new();
        private ObservableCollection<LPRItem> _filteredItems = new();

        public LPR()
        {
            InitializeComponent();

            LoadColumnSelector();

            // Temporary sample data (replace with API call)
            LoadSampleData();

            JobsGrid.ItemsSource = _filteredItems;
        }

        private void LoadColumnSelector()
        {
            ColumnSelector.ItemsSource = new List<string>
            {
                "Srl","Lpr_No","Date","Indent_No","Job_No_Comp_Dt","Ohs","Page",
                "Part_No","Nomen","Qty","Recd","So","So_Date","Vend","Rate","Status"
            };

            ColumnSelector.SelectedIndex = 0;
        }

        private void LoadSampleData()
        {
            _allItems = new ObservableCollection<LPRItem>
            {
                new LPRItem { Srl = 1, Lpr_No="LP/01", Date=DateTime.Now.AddDays(-3), Indent_No="IND01",
                              Job_No_Comp_Dt="J-10", Ohs="OK", Page="8", Part_No="P100",
                              Nomen="Bolt", Qty=5, Recd=5, So="SO10", So_Date=DateTime.Now,
                              Vend="ABC Ltd", Rate=89.2, Status="Completed"},

                new LPRItem { Srl = 2, Lpr_No="LP/02", Date=DateTime.Now.AddDays(-12), Indent_No="IND02",
                              Job_No_Comp_Dt="J-11", Ohs="Pending", Page="9", Part_No="P200",
                              Nomen="Nut", Qty=20, Recd=10, So="SO11", So_Date=DateTime.Now.AddDays(-10),
                              Vend="XYZ Ltd", Rate=45.0, Status="Pending"}
            };

            foreach (var item in _allItems)
                _filteredItems.Add(item);
        }

        private void ApplyFilters()
        {
            if (_allItems.Count == 0) return;

            string selectedCol = ColumnSelector.SelectedItem?.ToString();
            string search = SearchBox.Text?.Trim().ToLower() ?? "";

            _filteredItems.Clear();

            IEnumerable<LPRItem> query = _allItems;

            // Last X days filter
            var selectedDaysItem = (DaysFilterBox.SelectedItem as ComboBoxItem)?.Content?.ToString();
            if (selectedDaysItem != "All")
            {
                int days = selectedDaysItem switch
                {
                    "Last 7 Days" => 7,
                    "Last 15 Days" => 15,
                    "Last 30 Days" => 30,
                    "Last 90 Days" => 90,
                    _ => 0
                };

                DateTime cutoff = DateTime.Now.AddDays(-days);
                query = query.Where(i => i.Date >= cutoff);
            }

            // Text search
            if (!string.IsNullOrEmpty(search))
            {
                query = query.Where(item =>
                {
                    var prop = typeof(LPRItem).GetProperty(selectedCol);
                    var val = prop?.GetValue(item)?.ToString()?.ToLower() ?? "";
                    return val.Contains(search);
                });
            }

            foreach (var i in query)
                _filteredItems.Add(i);
        }

        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            ApplyFilters();
        }

        private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            ApplyFilters();
        }

        private void LogoButton_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.GoBack();
        }
    }
}
