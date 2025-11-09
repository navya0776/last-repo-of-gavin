using IMS.Models;
using IMS.Services;
using System;
using System.Windows;
using System.Windows.Controls;

namespace IMS.Windows
{
    public partial class AddLedgerWindow : Window
    {
        public LedgerItem CreatedLedger { get; private set; }

        public AddLedgerWindow()
        {
            InitializeComponent();
        }

        private async void Save_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                var ledger = new LedgerItem
                {
                    idx = 0,
                    ledger_page = LedgerPage.Text,
                    ohs_number = OHSNo.Text,
                    isg_number = ISGNo.Text,
                    ssg_number = SSGNo.Text,
                    part_number = PartNo.Text,
                    nomenclature = Nomen.Text,
                    a_u = AU.Text,
                    no_off = int.TryParse(NoOff.Text, out var noOffVal) ? noOffVal : 0,
                    scl_auth = int.TryParse(SclAuth.Text, out var sclVal) ? sclVal : 0,
                    unsv_stock = int.TryParse(UnsvStock.Text, out var unsvVal) ? unsvVal : 0,
                    rep_stock = int.TryParse(RepStock.Text, out var repVal) ? repVal : 0,
                    serv_stock = int.TryParse(ServStock.Text, out var servVal) ? servVal : 0,
                    msc = (MSC.SelectedItem as ComboBoxItem)?.Content.ToString() ?? "M",
                    ved = (VED.SelectedItem as ComboBoxItem)?.Content.ToString() ?? "V",
                    in_house = (InHouse.SelectedItem as ComboBoxItem)?.Content.ToString() ?? "in_house",
                    bin_number = BinNumber.Text,
                    group = Group.Text,
                    cos_sec = COSSec.Text,
                    cab_no = CabNo.Text,
                    old_pg_ref = double.TryParse(OldPgRef.Text, out var oldRef) ? oldRef : 0,
                    Assy_Comp = (AssyComp.SelectedItem as ComboBoxItem)?.Content.ToString() ?? "Assembly",
                    Re_ord_lvl = int.TryParse(ReOrdLvl.Text, out var reOrdVal) ? reOrdVal : 0,
                    safety_stk = int.TryParse(SafetyStock.Text, out var safetyVal) ? safetyVal : 0
                };

                var result = await ApiService.CreateLedgerAsync(ledger);

                if (result != null)
                {
                    MessageBox.Show("✅ Ledger entry added successfully!");
                    CreatedLedger = result;
                    DialogResult = true;
                    Close();
                }
                else
                {
                    MessageBox.Show("❌ Failed to add ledger entry. Check backend logs.");
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}
