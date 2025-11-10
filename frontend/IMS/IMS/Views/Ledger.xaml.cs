// File: Views/Ledger.xaml.cs
using DocumentFormat.OpenXml.Office.Word;
using IMS.Helpers;
using IMS.Models;
using IMS.Services;
using IMS.Windows;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

namespace IMS.Views
{
    public partial class Ledger : Page
    {
        private Dictionary<string, List<string>> _storesMeta = new(); // store -> substores list
        private ObservableCollection<LedgerItem> _activeLedgerItems = new();
        private string _currentStore = null;
        private string _currentSubStore = null;

        // editing item
        private LedgerItem _editing = null;

        // Set your API base here
        private const string ApiBaseUrl = "http://localhost:8000";

        // Mock store → sub-store data


        public Ledger()
        {
            InitializeComponent();
            _ = TestBackendConnectionAsync();
            // If you already have a cookie from login flow, set it:
            //_api.SetAuthCookie("session", "<cookie-value>", "api.example.com");

            ColumnSelector.ItemsSource = typeof(LedgerItem).GetProperties().Select(p => p.Name).ToList();
            ColumnSelector.SelectedIndex = 0;

            // initial load
            _ = LoadStoresAndInitialDataAsync();
        }

        private async Task TestBackendConnectionAsync()
        {
            try
            {
                // Step 1: Try login
                bool success = await ApiService.LoginAsync("navya", "123456");
                if (!success)
                {
                    MessageBox.Show("❌ Login failed — check backend logs!");
                    return;
                }

                // Step 2: Print cookies to console
                ApiService.PrintCookies();

                // Step 3: Try fetching stores
                var stores = await ApiService.GetStoresAsync();

                if (stores == null || stores.Count == 0)
                {
                    MessageBox.Show("⚠️ No stores found — maybe backend has no data yet?");
                }
                else
                {
                    var msg = $"✅ Got {stores.Count} stores:\n" +
                              string.Join("\n", stores.Select(s => $"• {s.store} ({s.substores.Count} substores)"));
                    MessageBox.Show(msg);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"🔥 Exception: {ex.Message}");
            }
        }


        private async Task LoadStoresAndInitialDataAsync()
        {
            try
            {
                // 1) load stores from backend
                var stores = await ApiService.GetStoresAsync();
                //MessageBox.Show($"Fetched {stores.Count} stores");  // 💖 Add this line
                                                                      // returns list of (store, substores)
                _storesMeta.Clear();
                foreach (var (store, subs) in stores)
                {
                    _storesMeta[store] = subs;
                }

                // populate TreeView
                PopulateStoresTree();

                // optionally load first store/substore ledger automatically (if exists)
                var first = _storesMeta.FirstOrDefault();
                if (!string.IsNullOrEmpty(first.Key) && first.Value.Any())
                {
                    await SelectStoreSubstoreAsync(first.Key, first.Value.First());
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to load stores: {ex.Message}");
            }
        }



        #region TreeView population & selection
        private void PopulateStoresTree()
        {
            StoresTree.Items.Clear();
            foreach (var kv in _storesMeta)
            {
                var storeItem = new TreeViewItem { Header = kv.Key };
                foreach (var sub in kv.Value)
                {
                    var subItem = new TreeViewItem { Header = sub };
                    storeItem.Items.Add(subItem);
                }
                StoresTree.Items.Add(storeItem);
                //MessageBox.Show($"Store: {kv.Key} → {kv.Value.Count} substores");

            }
        }

        private async Task SelectStoreSubstoreAsync(string store, string substore)
        {
            _currentStore = store;
            _currentSubStore = substore;
            await LoadLedgerForCurrentSelectionAsync();
        }

        private async void StoresTree_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
        {
            if (StoresTree.SelectedItem is TreeViewItem tvi)
            {
                // detect whether it's a sub-store leaf or a store node (store node has items)
                if (tvi.Parent is TreeViewItem)
                {
                    // If parent is TreeViewItem, this is a child — but TreeView structure depends,
                    // so let's find the selected store/substore by walking up
                    string sub = tvi.Header?.ToString();
                    string store = null;
                    if (tvi.Parent is TreeViewItem parent)
                        store = parent.Header?.ToString();

                    if (!string.IsNullOrEmpty(store) && !string.IsNullOrEmpty(sub))
                    {
                        await SelectStoreSubstoreAsync(store, sub);
                    }
                }
                else
                {
                    // store node selected (no substore)
                    _currentStore = tvi.Header?.ToString();
                    _currentSubStore = null;
                    LedgerDataGrid.ItemsSource = null;
                }
            }
        }
        #endregion

        #region Load ledger from backend
        private async Task LoadLedgerForCurrentSelectionAsync()
        {
            if (string.IsNullOrEmpty(_currentStore) || string.IsNullOrEmpty(_currentSubStore))
            {
                LedgerDataGrid.ItemsSource = null;
                return;
            }

            try
            {
                var items = await ApiService.GetLedgerAsync(_currentStore);
                _activeLedgerItems = new ObservableCollection<LedgerItem>(items);
                LedgerDataGrid.ItemsSource = _activeLedgerItems;
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Failed to load ledger: {ex.Message}");
            }
        }
        #endregion

        #region Add / Update via overlay
        private async void Add_Click(object sender, RoutedEventArgs e)
        {
            var addWindow = new IMS.Windows.AddLedgerWindow();
            addWindow.Owner = Window.GetWindow(this);

            if (addWindow.ShowDialog() == true)
            {
                var newLedger = addWindow.CreatedLedger;
                if (newLedger != null)
                {
                    _activeLedgerItems.Add(newLedger);
                    LedgerDataGrid.ItemsSource = null;
                    LedgerDataGrid.ItemsSource = _activeLedgerItems;
                }
            }
        }


        private void Update_Click(object sender, RoutedEventArgs e)
        {
            if (LedgerDataGrid.SelectedItem is LedgerItem selected)
            {
                var win = new IMS.Windows.UpdateLedgerWindow(selected)
                {
                    Owner = Window.GetWindow(this)
                };

                if (win.ShowDialog() == true)
                {
                    _ = LoadLedgerForCurrentSelectionAsync();
                }
            }
            else
            {
                MessageBox.Show("Please select a ledger page to update.");
            }
        }


   
        #endregion

        #region Search (client-side)
        private void Search_Click(object sender, RoutedEventArgs e) => ApplyFilter();
        private void SearchBox_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (e.Key == System.Windows.Input.Key.Enter) ApplyFilter();
        }

        private void ApplyFilter()
        {
            var term = (SearchTextBox.Text ?? "").Trim();
            var col = ColumnSelector.SelectedItem as string;
            if (string.IsNullOrWhiteSpace(col) || string.IsNullOrWhiteSpace(term) || _activeLedgerItems == null) return;

            var filtered = _activeLedgerItems.Where(x =>
            {
                var p = typeof(LedgerItem).GetProperty(col);
                if (p == null) return false;
                var val = p.GetValue(x)?.ToString() ?? "";
                return val.IndexOf(term, StringComparison.OrdinalIgnoreCase) >= 0;
            }).ToList();

            LedgerDataGrid.ItemsSource = filtered;
        }

        private void Clear_Click(object sender, RoutedEventArgs e)
        {
            SearchTextBox.Text = "";
            if (_activeLedgerItems != null) LedgerDataGrid.ItemsSource = _activeLedgerItems;
        }
        #endregion

        #region Export (uses FieldSelectionWindow & ExcelExporter)
        private void ExportToXlsx_Click(object sender, RoutedEventArgs e)
        {
            if (string.IsNullOrEmpty(_currentSubStore))
            {
                MessageBox.Show("Please select an equipment (sub-store) to export.");
                return;
            }

            var colInfos = LedgerDataGrid.Columns
                .OfType<DataGridTextColumn>()
                .Select(c =>
                {
                    var binding = c.Binding as Binding;
                    return new
                    {
                        Header = c.Header?.ToString() ?? "",
                        Binding = binding?.Path?.Path ?? ""
                    };
                })
                .ToList();


            var dlg = new FieldSelectionWindow();
            dlg.SelectedFields(colInfos.Select(x => (x.Header, x.Binding)));
            dlg.Owner = Window.GetWindow(this);
            if (dlg.ShowDialog() != true) return;

            var selectedHeaders = dlg.SelectedHeaders;
            if (selectedHeaders == null || selectedHeaders.Count == 0) { MessageBox.Show("No columns selected."); return; }

            // Map selected header -> binding/property (if binding empty, try to use header as property)
            var headerToProp = colInfos.ToDictionary(x => x.Header, x => x.Binding);
            var propNames = selectedHeaders.Select(h => headerToProp.ContainsKey(h) && !string.IsNullOrEmpty(headerToProp[h]) ? headerToProp[h] : h).ToList();
            var selectedHeadersObj = selectedHeaders.Cast<object>().ToList();
            var propNamesObj = propNames.Cast<object>().ToList();
            var items = LedgerDataGrid.ItemsSource as IEnumerable<LedgerItem> ?? _activeLedgerItems;
            var sfd = new Microsoft.Win32.SaveFileDialog { Filter = "Excel Workbook (*.xlsx)|*.xlsx", FileName = "LedgerExport.xlsx" };
            if (sfd.ShowDialog() != true) return;

            try
            {
                ExcelExporter.Export(sfd.FileName, items, selectedHeaders, propNamesObj);
                MessageBox.Show("Export successful.");
            }
            catch (Exception ex)
            {
                MessageBox.Show("Export failed: " + ex.Message);
            }
        }
        #endregion

        private void ColumnSelector_SelectionChanged(object sender, SelectionChangedEventArgs e)

        { 
            var combo = sender as ComboBox;
            var selected = combo?.SelectedItem;
        }

        private void Reports_Click(object sender, RoutedEventArgs e)
        {
            var reportsWindow = new ReportsPageLedger
            {
                Owner = Window.GetWindow(this)  // makes it modal to parent
            };

            bool? result = reportsWindow.ShowDialog();

            if (result == true)
            {
                string selectedReport = reportsWindow.SelectedReport;
                MessageBox.Show($"You selected: {selectedReport}", "Report Selected");

                // TODO: Call backend analysis API or export logic here
            }
        }

        private void LedgerDataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {

        }

        private void FilterButton_Click(object sender, RoutedEventArgs e)
        {
            FilterPopup.IsOpen = !FilterPopup.IsOpen;
        }

        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            var term = (SearchTextBox.Text ?? "").Trim();

            // if nothing typed, show all ledgers again
            if (string.IsNullOrWhiteSpace(term))
            {
                LedgerDataGrid.ItemsSource = _activeLedgerItems;
                return;
            }

            var col = ColumnSelector.SelectedItem as string;
            if (string.IsNullOrWhiteSpace(col))
                return;

            // filter dynamically based on the selected column
            var filtered = _activeLedgerItems.Where(x =>
            {
                var p = typeof(LedgerItem).GetProperty(col);
                if (p == null) return false;
                var val = p.GetValue(x)?.ToString() ?? "";
                return val.IndexOf(term, StringComparison.OrdinalIgnoreCase) >= 0;
            }).ToList();

            LedgerDataGrid.ItemsSource = filtered;
        }

    }


}


