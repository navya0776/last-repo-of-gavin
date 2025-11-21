using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Collections.ObjectModel;
using System.Windows.Controls;

namespace IMS.Windows
{
    public partial class FieldSelectionWindow : Window
    {
        public class ColumnOption
        {
            public string HeaderText { get; set; }
            public string BindingPath { get; set; } // kept for potential future use
            public bool IsSelected { get; set; }
        }

        private ObservableCollection<ColumnOption> _allOptions = new ObservableCollection<ColumnOption>();

        public List<string> SelectedHeaders =>
    _allOptions.Where(o => o.IsSelected).Select(o => o.HeaderText).ToList();

        public void SelectedFields(IEnumerable<(string header, string binding)> columns)
        {
            InitializeComponent();

            // create options from provided list (header + binding)
            foreach (var (header, binding) in columns)
            {
                _allOptions.Add(new ColumnOption
                {
                    HeaderText = header,
                    BindingPath = binding,
                    IsSelected = true
                });
            }

            ColumnsItemsControl.ItemsSource = _allOptions;
            UpdateSelectAllBox();
        }


        private void Ok_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = true;
            Close();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }


        private void SelectAllBox_Checked(object sender, RoutedEventArgs e)
        {
            foreach (var o in _allOptions) o.IsSelected = true;
            ColumnsItemsControl.Items.Refresh();
        }

        private void SelectAllBox_Unchecked(object sender, RoutedEventArgs e)
        {
            foreach (var o in _allOptions) o.IsSelected = false;
            ColumnsItemsControl.Items.Refresh();
        }

        private void UpdateSelectAllBox()
        {
            if (_allOptions.Count == 0) { SelectAllBox.IsChecked = false; return; }
            var all = _allOptions.All(x => x.IsSelected);
            var none = _allOptions.All(x => !x.IsSelected);
            SelectAllBox.IsChecked = all ? true : (none ? false : (bool?)null);
        }
    }
}

