using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace IMS.SAPEAAviews
{
    /// <summary>
    /// Interaction logic for Vendor.xaml
    /// </summary>
    public partial class Vendor : Page
    {

        
            private List<ShortOrderItem> _allData = new();
            private List<ShortOrderItem> _filteredData = new();

            public Vendor()
            {
                InitializeComponent();
                LoadDummyData();
                LoadColumnSelector();
                LoadSO_All_Columns();
                JobsGrid.ItemsSource = _filteredData;
            }


            // ================== LOAD SAMPLE DATA ==================
            private void LoadDummyData()
            {
                _allData = new List<ShortOrderItem>()
            {
                new ShortOrderItem
                {
                    Srl = 1, Lpr_No="0001", Date="24/04/2025",
                    Indent_No="IND001", Job_No_Comp_Dt="---",
                    Ohs="MT", Page="1", Part_No="PN01", Nomen="Bolt",
                    Qty=10, Recd=5, So="SO001", So_Date="24/04/2025",
                    Vend="ABC", Rate="200", Status="Pending"
                },
                new ShortOrderItem
                {
                    Srl = 2, Lpr_No="0002", Date="25/04/2025",
                    Indent_No="IND002", Job_No_Comp_Dt="---",
                    Ohs="EM", Page="2", Part_No="PN10", Nomen="Nut",
                    Qty=12, Recd=12, So="SO002", So_Date="25/04/2025",
                    Vend="XYZ", Rate="350", Status="Completed"
                }
            };

                _filteredData = _allData.ToList();
            }


            // ================== COLUMN SELECTOR ==================
            private void LoadColumnSelector()
            {
                ColumnSelector.ItemsSource = typeof(ShortOrderItem)
                    .GetProperties()
                    .Select(x => x.Name)
                    .ToList();

                ColumnSelector.SelectedIndex = 0;
            }


            // ================== LEFT MENU: SO >> ALL ==================
            private void SO_All_Click(object sender, RoutedEventArgs e)
            {
                LoadSO_All_Columns();
                JobsGrid.ItemsSource = _filteredData;
            }

            // ================== LEFT MENU: SO >> NO ==================
            private void SO_No_Click(object sender, RoutedEventArgs e)
            {
                LoadSO_No_Columns();

                JobsGrid.ItemsSource = _allData
                    .Select(x => new
                    {
                        x.So,
                        x.So_Date,
                        x.Lpr_No,
                        x.Nomen,
                        x.Qty,
                        x.Rate,
                        x.Status
                    }).ToList();
            }


            // ================== BUILD COLUMNS FOR SO >> ALL ==================
            private void LoadSO_All_Columns()
            {
                JobsGrid.Columns.Clear();

                AddColumn("SO No", "SO_No");
                AddColumn("SO Date", "SO_Date");
                AddColumn("Date", "Date");
                AddColumn("Indent No", "Indent_No");
                AddColumn("Amount(O)", "amount_o");
                AddColumn("Amount(R)", "amount_r");
                AddColumn("Vend", "vend");
                AddColumn("Bill", "bill");
                AddColumn("Bill date", "bill_date");
                AddColumn("Bill Amt", "bill_amt");
                AddColumn("Firm No", "firm_no");
                AddColumn("Date", "date");
            }

            // ================== BUILD COLUMNS FOR SO >> NO ==================
            private void LoadSO_No_Columns()
            {
                JobsGrid.Columns.Clear();

                AddColumn("Srl", "Srl");
                AddColumn("LPR No", "Lpr_No");
                AddColumn("Date", "Date");
                AddColumn("Indent No", "Indent_No");
                AddColumn("Job No/Comp Dt", "Job_No_Comp_Dt");
                AddColumn("OHS", "Ohs");
                AddColumn("Page", "Page");
                AddColumn("Part No", "Part_No");
                AddColumn("Nomen", "Nomen");
                AddColumn("Qty", "Qty");
                AddColumn("Recd", "Recd");
                AddColumn("SO", "So");
                AddColumn("SO Date", "So_Date");
                AddColumn("Vend", "Vend");
                AddColumn("Rate", "Rate");
                AddColumn("Status", "Status");
            }


            // Helper to build column
            private void AddColumn(string header, string binding)
            {
                JobsGrid.Columns.Add(new DataGridTextColumn
                {
                    Header = header,
                    Binding = new System.Windows.Data.Binding(binding),
                    MinWidth = 100
                });
            }


            // ================== SEARCH ==================
            private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
            {
                if (string.IsNullOrWhiteSpace(SearchBox.Text))
                {
                    _filteredData = _allData.ToList();
                }
                else
                {
                    string col = ColumnSelector.SelectedItem.ToString();
                    string term = SearchBox.Text.ToLower();

                    _filteredData = _allData
                        .Where(x =>
                        {
                            var prop = typeof(ShortOrderItem).GetProperty(col);
                            if (prop == null) return false;
                            string val = prop.GetValue(x)?.ToString()?.ToLower() ?? "";
                            return val.Contains(term);
                        }).ToList();
                }

                JobsGrid.ItemsSource = _filteredData;
            }


            // ================== DAYS FILTER ==================
            private void DaysFilterBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
            {
                string selected = (DaysFilterBox.SelectedItem as ComboBoxItem).Content.ToString();

                if (selected == "All")
                {
                    _filteredData = _allData.ToList();
                }
                else
                {
                    int days = int.Parse(selected.Split(' ')[1]);

                    _filteredData = _allData
                        .Where(x =>
                        {
                            DateTime dt;
                            if (DateTime.TryParse(x.Date, out dt))
                            {
                                return dt >= DateTime.Now.AddDays(-days);
                            }
                            return false;
                        }).ToList();
                }

                JobsGrid.ItemsSource = _filteredData;
            }


            private void LogoButton_Click(object sender, RoutedEventArgs e)
            {
                NavigationService.GoBack();
            }
        }
    

}
