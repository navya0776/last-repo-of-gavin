// File: Views/Ledger.xaml.cs
using DocumentFormat.OpenXml.Office.Word;
using IMS.Helpers;
using IMS.Models;
using IMS.Services;
using IMS.Windows;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Threading;

namespace IMS.Views
{
    public partial class Ledger : Page
    {
        private static Random R = new Random();

        // Mock ledger: Store -> Equipment (substore) -> List<LedgerItem>
        private Dictionary<string, Dictionary<string, List<LedgerItem>>> _mockLedger = new();

        // store -> substores list
        private Dictionary<string, List<string>> _storesMeta = new();
        private ObservableCollection<LedgerItem> _activeLedgerItems = new();
        private string _currentStore = null;
        private string _currentSubStore = null;

        // editing item
        private LedgerItem _editing = null;

        // Set your API base here
        private const string ApiBaseUrl = "http://localhost:8000";

        public Ledger()
        {
            InitializeComponent();

            // Load mock data (local only)
            LoadMassiveMockLedger();

            ColumnSelector.ItemsSource = typeof(LedgerItem).GetProperties().Select(p => p.Name).ToList();
            ColumnSelector.SelectedIndex = 0;

            // initial load (now uses mock data)
            _ = LoadStoresAndInitialDataAsync();
        }

        /// <summary>
        /// Generates a large in-memory mock ledger:
        ///  - ~20 stores
        ///  - each store has 5–12 equipments
        ///  - each equipment has 50–200 items
        /// </summary>
        private void LoadMassiveMockLedger()
        {
            string[] storeNames = Enumerable.Range(1, 20)
                .Select(i => $"Store {i}")
                .ToArray();

            string[] equipmentNames = {
                "Compressor", "Generator", "Cooling Unit", "Switchboard", "Power Panel",
                "Water Pump", "Valve Set", "Control Unit", "Gearbox", "Battery Pack",
                "Pressure System", "Hydraulic Set", "Ignition Panel", "Sensor Suite"
            };

            string[] vedValues = { "V", "E", "D" };
            string[] mscValues = { "M", "S", "C" };
            string[] groups = { "A", "B", "C", "D" };
            string[] auTypes = { "EA", "SET", "PCS" };

            _mockLedger = new Dictionary<string, Dictionary<string, List<LedgerItem>>>();

            foreach (var store in storeNames)
            {
                int eqCount = R.Next(5, 12); // 5–12 equipments per store

                var equipmentDict = new Dictionary<string, List<LedgerItem>>();

                for (int e = 0; e < eqCount; e++)
                {
                    string eqName = $"{equipmentNames[R.Next(equipmentNames.Length)]} {R.Next(100, 999)}";

                    int itemCount = R.Next(50, 200); // 50–200 ledger items

                    var ledgerItems = new List<LedgerItem>();

                    for (int i = 1; i <= itemCount; i++)
                    {
                        ledgerItems.Add(new LedgerItem
                        {
                            idx = i,
                            ledger_page = $"{R.Next(1, 999):D3}",
                            ohs_number = $"OHS-{R.Next(1000, 9999)}",
                            isg_number = $"ISG-{R.Next(1000, 9999)}",
                            ssg_number = $"SSG-{R.Next(1000, 9999)}",
                            part_number = $"PN-{R.Next(10000, 99999)}",
                            nomenclature = $"Part {R.Next(1, 999)} for {eqName}",
                            a_u = auTypes[R.Next(auTypes.Length)],
                            no_off = R.Next(1, 50),
                            scl_auth = R.Next(0, 2) == 0 ? 0 : R.Next(1, 50),
                            unsv_stock = R.Next(0, 30),
                            rep_stock = R.Next(0, 20),
                            serv_stock = R.Next(0, 40),
                            msc = mscValues[R.Next(mscValues.Length)],
                            ved = vedValues[R.Next(vedValues.Length)],
                            in_house = $"{R.Next(1, 999):D3}",
                            bin_number = $"BIN-{R.Next(1, 300)}",
                            group = groups[R.Next(groups.Length)],
                            cds_unsv_stock = R.Next(0, 20),
                            cds_rep_stock = R.Next(0, 15),
                            cds_serv_stock = R.Next(0, 25),
                            lpp = $"{R.Next(1, 999):D3}",
                            rate = R.Next(50, 5000),
                            rmks = R.Next(0, 4) == 0 ? "Critical item" : "",
                            lpp_dt = DateTime.Now.AddDays(-R.Next(10, 1000)).ToString("dd-MM-yyyy")
                        });
                    }

                    equipmentDict[eqName] = ledgerItems;
                }

                _mockLedger[store] = equipmentDict;
            }

            // Load store → equipment structure for TreeView
            _storesMeta = _mockLedger.ToDictionary(
                store => store.Key,
                store => store.Value.Keys.ToList()
            );

            PopulateStoresTree();
        }

        // Backend test helper (kept but commented)
        //private async Task TestBackendConnectionAsync()
        //{
        //    try
        //    {
        //        bool success = await ApiService.LoginAsync("navya", "123456");
        //        if (!success) return;
        //
        //        ApiService.PrintCookies();
        //
        //        var stores = await ApiService.GetStoresAsync();
        //        _storesMeta.Clear();
        //        foreach (var (store, subs) in stores)
        //            _storesMeta[store] = subs;
        //
        //        PopulateStoresTree();
        //    }
        //    catch (Exception ex)
        //    {
        //    }
        //}

        private async Task LoadStoresAndInitialDataAsync()
        {
            try
            {
                // ✅ BACKEND DISABLED FOR NOW
                // var stores = await ApiService.GetStoresAsync();
                // _storesMeta.Clear();
                // foreach (var (store, subs) in stores)
                // {
                //     _storesMeta[store] = subs;
                // }

                // We already populated _storesMeta from mock:
                PopulateStoresTree();

                // Load first store/substore (from mock)
                var first = _storesMeta.FirstOrDefault();
                if (!string.IsNullOrEmpty(first.Key) && first.Value.Any())
                {
                    await SelectStoreSubstoreAsync(first.Key, first.Value.First());
                }
            }
            catch (Exception ex)
            {
                //MessageBox.Show($"Failed to load stores: {ex.Message}");
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
            }
        }

        private async Task SelectStoreSubstoreAsync(string store, string substore)
        {
            _currentStore = store;
            _currentSubStore = substore;
            await LoadLedgerForCurrentSelectionAsync();
        }

        private void StoresTree_SelectedItemChanged(object sender, RoutedPropertyChangedEventArgs<object> e)
        {
            if (StoresTree.SelectedItem is TreeViewItem tvi)
            {
                // If parent is TreeViewItem -> this is a substore (equipment)
                if (tvi.Parent is TreeViewItem parent)
                {
                    string sub = tvi.Header.ToString();
                    string store = parent.Header.ToString();
                    LoadMockLedgerFor(store, sub);
                }
                else
                {
                    // Store clicked — clear ledger
                    LedgerDataGrid.ItemsSource = null;
                }
            }
        }

        private void LoadMockLedgerFor(string store, string substore)
        {
            if (_mockLedger.ContainsKey(store) &&
                _mockLedger[store].ContainsKey(substore))
            {
                _activeLedgerItems = new ObservableCollection<LedgerItem>(_mockLedger[store][substore]);
                LedgerDataGrid.ItemsSource = _activeLedgerItems;

                _currentStore = store;
                _currentSubStore = substore;
            }
        }

        #endregion

        #region Load ledger (mock instead of backend)
        private Task LoadLedgerForCurrentSelectionAsync()
        {
            if (string.IsNullOrEmpty(_currentStore) || string.IsNullOrEmpty(_currentSubStore))
            {
                LedgerDataGrid.ItemsSource = null;
                return Task.CompletedTask;
            }

            // ✅ Use mock data instead of backend:
            LoadMockLedgerFor(_currentStore, _currentSubStore);

            // ❌ Old backend call kept but commented:
            // try
            // {
            //     var items = await ApiService.GetLedgerAsync(_currentStore);
            //     _activeLedgerItems = new ObservableCollection<LedgerItem>(items);
            //     LedgerDataGrid.ItemsSource = _activeLedgerItems;
            // }
            // catch (Exception ex)
            // {
            // }

            return Task.CompletedTask;
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

                    // also update our mock data store
                    if (!string.IsNullOrEmpty(_currentStore) && !string.IsNullOrEmpty(_currentSubStore))
                    {
                        if (_mockLedger.ContainsKey(_currentStore) &&
                            _mockLedger[_currentStore].ContainsKey(_currentSubStore))
                        {
                            _mockLedger[_currentStore][_currentSubStore].Add(newLedger);
                        }
                    }

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
                    // For mock: data already updated via binding (if your window modifies the same instance)
                    // Refresh grid:
                    LedgerDataGrid.ItemsSource = null;
                    LedgerDataGrid.ItemsSource = _activeLedgerItems;

                    // If you want, you can re-sync mock backing store as well
                    // (but reference type updates already reflect there).
                    // _ = LoadLedgerForCurrentSelectionAsync();
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
            if (selectedHeaders == null || selectedHeaders.Count == 0)
            {
                MessageBox.Show("No columns selected.");
                return;
            }

            var headerToProp = colInfos.ToDictionary(x => x.Header, x => x.Binding);
            var propNames = selectedHeaders.Select(h =>
                headerToProp.ContainsKey(h) && !string.IsNullOrEmpty(headerToProp[h])
                    ? headerToProp[h]
                    : h).ToList();

            var items = LedgerDataGrid.ItemsSource as IEnumerable<LedgerItem> ?? _activeLedgerItems;

            var sfd = new Microsoft.Win32.SaveFileDialog
            {
                Filter = "Excel Workbook (*.xlsx)|*.xlsx",
                FileName = "LedgerExport.xlsx"
            };
            if (sfd.ShowDialog() != true) return;

            try
            {
                ExcelExporter.Export(sfd.FileName, items, selectedHeaders, propNames.Cast<object>().ToList());
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

        private void LedgerDataGrid_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
        }

        #region Filter Popup & SearchBox live filter
        private void FilterButton_Click(object sender, RoutedEventArgs e)
        {
            FilterPopup.IsOpen = !FilterPopup.IsOpen;
        }

        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            var term = (SearchTextBox.Text ?? "").Trim();

            if (string.IsNullOrWhiteSpace(term))
            {
                LedgerDataGrid.ItemsSource = _activeLedgerItems;
                return;
            }

            var col = ColumnSelector.SelectedItem as string;
            if (string.IsNullOrWhiteSpace(col))
                return;

            var filtered = _activeLedgerItems.Where(x =>
            {
                var p = typeof(LedgerItem).GetProperty(col);
                if (p == null) return false;
                var val = p.GetValue(x)?.ToString() ?? "";
                return val.IndexOf(term, StringComparison.OrdinalIgnoreCase) >= 0;
            }).ToList();

            LedgerDataGrid.ItemsSource = filtered;
        }
        #endregion

        #region Reports (all on mock data)
        private async void Reports_Click(object sender, RoutedEventArgs e)
        {
            var reportsWindow = new ReportsPageLedger
            {
                Owner = Window.GetWindow(this)
            };

            bool? result = reportsWindow.ShowDialog();
            if (result != true) return;

            string selectedReport = reportsWindow.SelectedReport;

            if (_currentSubStore == null)
                return;

            switch (selectedReport)
            {
                case "Current Stock Report":
                    await ShowCurrentStockReport();
                    break;
                case "MSC Analysis Report":
                    await ShowMSCAnalysisReport();
                    break;
                case "VED Analysis Report":
                    await ShowVEDAnalysisReport();
                    break;
                case "Vital":
                    await ShowVitalReport();
                    break;
                case "Desiraable":
                    await ShowDesirableReport();
                    break;
                case "Essential":
                    await ShowEssentialReport();
                    break;
                case "Scaled items":
                    await ShowScaledItemsReport();
                    break;
                case "Non-Scaled Items":
                    await ShowNonScaledItemsReport();
                    break;
                case "Must Change":
                    await ShowMustChangeReport();
                    break;
                case "Should Change":
                    await ShowShouldChangeReport();
                    break;
                case "Could Change":
                    await ShowCouldChangeReport();
                    break;
                default:
                    MessageBox.Show("Unknown report type selected.");
                    break;
            }
        }

        private Task ShowCurrentStockReport()
        {
            var rows = _activeLedgerItems
                .Select((item, idx) => new
                {
                    Index = idx + 1,
                    PartNo = item.part_number,
                    Nomenclature = item.nomenclature,
                    A_U = item.a_u,
                    TotalStock = item.unsv_stock + item.rep_stock + item.serv_stock
                })
                .ToList();

            string title = $"CURRENT STOCK REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);

            return Task.CompletedTask;
        }

        private async Task ShowMSCAnalysisReport()
        {
            var items = _activeLedgerItems;

            var rows = items.Select((x, i) => new
            {
                SrlNo = i + 1,
                PartNo = x.part_number,
                Nomenclature = x.nomenclature,
                MSC = x.msc
            }).Where(r => !string.IsNullOrEmpty(r.MSC)).ToList();

            string title = $"MSC ANALYSIS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowVEDAnalysisReport()
        {
            var rows = _activeLedgerItems.Select((x, i) => new
            {
                SrlNo = i + 1,
                PartNo = x.part_number,
                Nomenclature = x.nomenclature,
                VED = x.ved
            }).Where(r => !string.IsNullOrWhiteSpace(r.VED)).ToList();

            string title = $"VED ANALYSIS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowVitalReport()
        {
            var items = _activeLedgerItems.Where(x => x.ved == "V").ToList();
            var rows = items.Select((x, i) => new
            {
                SrlNo = i + 1,
                PartNo = x.part_number,
                Nomenclature = x.nomenclature,
                VED = x.ved
            }).ToList();
            string title = $"VITAL ITEMS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowDesirableReport()
        {
            var items = _activeLedgerItems.Where(x => x.ved == "D").ToList();
            var rows = items.Select((x, i) => new
            {
                SrlNo = i + 1,
                PartNo = x.part_number,
                Nomenclature = x.nomenclature,
                VED = x.ved
            }).ToList();
            string title = $"DESIRABLE ITEMS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowEssentialReport()
        {
            var items = _activeLedgerItems.Where(x => x.ved == "E").ToList();
            var rows = items.Select((x, i) => new
            {
                SrlNo = i + 1,
                PartNo = x.part_number,
                Nomenclature = x.nomenclature,
                VED = x.ved
            }).ToList();
            string title = $"ESSENTIAL ITEMS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowScaledItemsReport()
        {
            var items = _activeLedgerItems.Where(x => x.scl_auth > 0).ToList();
            var rows = items.Select((x, i) => new
            {
                SrlNo = i + 1,
                PartNo = x.part_number,
                Nomenclature = x.nomenclature,
                ScaleAuth = x.scl_auth
            }).ToList();
            string title = $"SCALED ITEMS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowNonScaledItemsReport()
        {
            var rows = _activeLedgerItems
                .Where(x => x.scl_auth == 0)
                .Select((x, i) => new
                {
                    SrlNo = i + 1,
                    PartNo = x.part_number,
                    Nomenclature = x.nomenclature,
                    ScaleAuth = x.scl_auth
                })
                .ToList();

            string title = $"NON-SCALED ITEMS REPORT : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowMustChangeReport()
        {
            var rows = _activeLedgerItems
                .Where(x => x.msc?.Equals("M", StringComparison.OrdinalIgnoreCase) == true)
                .Select((x, i) => new
                {
                    SrlNo = i + 1,
                    OSNo = x.ohs_number,
                    PartNo = x.part_number,
                    Nomenclature = x.nomenclature,
                    AU = x.a_u,
                    NoOff = x.no_off,
                    ScaleAuth = x.scl_auth,
                    CAT = x.msc
                })
                .ToList();

            string title = $"LIST OF MUST CHANGE ITEMS : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowShouldChangeReport()
        {
            var rows = _activeLedgerItems
                .Where(x => x.msc?.Equals("S", StringComparison.OrdinalIgnoreCase) == true)
                .Select((x, i) => new
                {
                    SrlNo = i + 1,
                    OSNo = x.ohs_number,
                    PartNo = x.part_number,
                    Nomenclature = x.nomenclature,
                    AU = x.a_u,
                    NoOff = x.no_off,
                    ScaleAuth = x.scl_auth,
                    CAT = x.group
                })
                .ToList();

            string title = $"LIST OF SHOULD CHANGE ITEMS : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }

        private async Task ShowCouldChangeReport()
        {
            var rows = _activeLedgerItems
                .Where(x => x.msc?.Equals("C", StringComparison.OrdinalIgnoreCase) == true)
                .Select((x, i) => new
                {
                    SrlNo = i + 1,
                    OSNo = x.ohs_number,
                    PartNo = x.part_number,
                    Nomenclature = x.nomenclature,
                    AU = x.a_u,
                    NoOff = x.no_off,
                    ScaleAuth = x.scl_auth,
                    CAT = x.group
                })
                .ToList();

            string title = $"LIST OF COULD CHANGE ITEMS : EQUIPMENT {_currentSubStore.ToUpper()}";
            ReportViewerWindow.ShowReport(title, rows);
        }
        #endregion

        #region Misc helpers (header/footer, dynamic reports etc.)
        private List<string> ShowColumnSelectionDialog()
        {
            var columns = LedgerDataGrid.Columns
                .OfType<DataGridTextColumn>()
                .Select(c =>
                {
                    var binding = c.Binding as Binding;
                    return new
                    {
                        Header = c.Header?.ToString() ?? "",
                        Property = binding?.Path?.Path ?? ""
                    };
                })
                .ToList();

            var dlg = new FieldSelectionWindow();
            dlg.SelectedFields(columns.Select(x => (x.Header, x.Property)));
            dlg.Owner = Window.GetWindow(this);

            if (dlg.ShowDialog() == true)
                return dlg.SelectedHeaders.ToList();

            return null;
        }

        private string BuildReportHeader(string reportName)
        {
            return
$@"Report: {reportName}
Store: {_currentStore}
Equipment (SubStore): {_currentSubStore}
Date: {DateTime.Now:dd MMM yyyy}";
        }

        private string BuildReportFooter(int count)
        {
            return
$@"Total Items: {count}
Generated by IMS";
        }

        private List<Dictionary<string, object>> BuildReportRows(
            IEnumerable<LedgerItem> source,
            List<string> selectedHeaders)
        {
            return source.Select((item, index) =>
            {
                var dict = new Dictionary<string, object>();
                dict["SrlNo"] = index + 1;

                foreach (var header in selectedHeaders)
                {
                    var prop = typeof(LedgerItem).GetProperty(header);
                    if (prop != null)
                        dict[header] = prop.GetValue(item);
                }

                return dict;
            }).ToList();
        }
        #endregion

        public event EventHandler ToggleSidebarRequested;

        private void MyButton_Click(object sender, RoutedEventArgs e)
        {
            ToggleSidebarRequested?.Invoke(this, EventArgs.Empty);
        }

        #region Fancy scrolling / drag scrolling
        private void Ledger_MouseWheel(object sender, MouseWheelEventArgs e)
        {
            var scrollViewer = FindParent<ScrollViewer>(LedgerDataGrid);
            if (scrollViewer == null) return;

            e.Handled = true;

            if (Keyboard.IsKeyDown(Key.LeftShift) || Keyboard.IsKeyDown(Key.RightShift))
            {
                scrollViewer.ScrollToHorizontalOffset(scrollViewer.HorizontalOffset - e.Delta);
            }
            else
            {
                double target = scrollViewer.VerticalOffset - (e.Delta * 0.4);
                AnimateScroll(scrollViewer, target);
            }
        }

        private void AnimateScroll(ScrollViewer viewer, double target)
        {
            target = Math.Max(0, Math.Min(target, viewer.ScrollableHeight));

            DispatcherTimer timer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(10)
            };

            timer.Tick += (s, e) =>
            {
                double diff = target - viewer.VerticalOffset;
                double step = diff * 0.25;

                if (Math.Abs(step) < 0.5)
                {
                    viewer.ScrollToVerticalOffset(target);
                    timer.Stop();
                }
                else
                {
                    viewer.ScrollToVerticalOffset(viewer.VerticalOffset + step);
                }
            };

            timer.Start();
        }

        private void Ledger_MouseLeftButtonDown(object sender, MouseButtonEventArgs e)
        {
            _ = Mouse.Capture(LedgerDataGrid);
        }

        private void Ledger_MouseMove(object sender, MouseEventArgs e)
        {
            if (e.LeftButton == MouseButtonState.Pressed)
            {
                var scrollViewer = FindParent<ScrollViewer>(LedgerDataGrid);
                if (scrollViewer == null) return;

                Point pos = e.GetPosition(LedgerDataGrid);

                double threshold = 30; // auto scroll zone height

                if (pos.Y < threshold)
                    scrollViewer.ScrollToVerticalOffset(scrollViewer.VerticalOffset - 2);

                if (pos.Y > LedgerDataGrid.ActualHeight - threshold)
                    scrollViewer.ScrollToVerticalOffset(scrollViewer.VerticalOffset + 2);
            }
        }

        private T FindParent<T>(DependencyObject child) where T : DependencyObject
        {
            DependencyObject parent = VisualTreeHelper.GetParent(child);

            while (parent != null && !(parent is T))
            {
                parent = VisualTreeHelper.GetParent(parent);
            }

            return parent as T;
        }

        private void LedgerDataGrid_PreviewMouseWheel(object sender, MouseWheelEventArgs e)
        {
            if (Keyboard.IsKeyDown(Key.LeftShift) || Keyboard.IsKeyDown(Key.RightShift))
            {
                var sv = GetScrollViewer(LedgerDataGrid);
                if (sv != null)
                    sv.ScrollToHorizontalOffset(sv.HorizontalOffset - e.Delta);

                e.Handled = true;
                return;
            }

            var scrollViewer = GetScrollViewer(LedgerDataGrid);
            if (scrollViewer != null)
            {
                scrollViewer.ScrollToVerticalOffset(scrollViewer.VerticalOffset - e.Delta);
                e.Handled = true;
            }
        }

        private ScrollViewer GetScrollViewer(DependencyObject obj)
        {
            if (obj is ScrollViewer) return (ScrollViewer)obj;

            for (int i = 0; i < VisualTreeHelper.GetChildrenCount(obj); i++)
            {
                var child = VisualTreeHelper.GetChild(obj, i);
                var result = GetScrollViewer(child);
                if (result != null) return result;
            }
            return null;
        }
        #endregion
    }
}
