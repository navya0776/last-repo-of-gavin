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

        // 🔥 Mock mode toggle (backend disabled)
        private bool UseMock = true;

        public AddLedgerWindow()
        {
            InitializeComponent();
        }

        private async void Save_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // ⭐ SAFE PARSING (prevents 422)
                int.TryParse(NoOff.Text, out int noOffVal);
                int.TryParse(SclAuth.Text, out int sclVal);
                int.TryParse(UnsvStock.Text, out int unsvVal);
                int.TryParse(RepStock.Text, out int repVal);
                int.TryParse(ServStock.Text, out int servVal);
                int.TryParse(ReOrdLvl.Text, out int reOrdVal);
                int.TryParse(SafetyStock.Text, out int safetyVal);
                double.TryParse(OldPgRef.Text, out double oldPgVal);

                // ⭐ BUILD LEDGER ITEM SAFELY
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

                    no_off = noOffVal,
                    scl_auth = sclVal,
                    unsv_stock = unsvVal,
                    rep_stock = repVal,
                    serv_stock = servVal,

                    msc = (MSC.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "M",
                    ved = (VED.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "V",
                    in_house = (InHouse.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "001",

                    bin_number = BinNumber.Text,
                    group = Group.Text,

                    cos_sec = COSSec.Text,
                    cab_no = CabNo.Text,
                    old_pg_ref = oldPgVal,
                    Assy_Comp = (AssyComp.SelectedItem as ComboBoxItem)?.Content?.ToString() ?? "COMP",

                    Re_ord_lvl = reOrdVal,
                    safety_stk = safetyVal,

                    // These backend fields are normally auto-filled.
                    // For mock mode we can set defaults so UI works.
                    cds_unsv_stock = 0,
                    cds_rep_stock = 0,
                    cds_serv_stock = 0,
                    lpp = "000",
                    rate = 0,
                    rmks = "",
                    lpp_dt = DateTime.Now.ToString("dd-MM-yyyy")
                };

                LedgerItem result = null;

                if (UseMock)
                {
                    // ❤️ Offline mode success
                    result = ledger;
                }
                else
                {
                    // REAL API CALL (DISABLED FOR NOW)
                    /*
                    result = await ApiService.CreateLedgerAsync(ledger);
                    */
                }

                if (result != null)
                {
                    CreatedLedger = result;
                    MessageBox.Show("✅ Ledger entry added successfully!");
                    DialogResult = true;
                    Close();
                }
                else
                {
                    MessageBox.Show("❌ Failed to add ledger entry.");
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
