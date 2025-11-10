using IMS.Models;
using IMS.Services;
using System;
using System.Windows;

namespace IMS.Windows
{
    public partial class UpdateLedgerWindow : Window
    {
        private readonly LedgerItem _item;

        public UpdateLedgerWindow(LedgerItem item)
        {
            InitializeComponent();
            _item = item;
            PopulateFields(item);
        }

        // ✅ Populate all fields correctly from model
        private void PopulateFields(LedgerItem it)
        {
            LedgerPage.Text = it.ledger_page;
            OHSNo.Text = it.ohs_number;
            ISGNo.Text = it.isg_number;
            SSGNo.Text = it.ssg_number;
            PartNo.Text = it.part_number;
            Nomen.Text = it.nomenclature;
            AU.Text = it.a_u;

            COSSec.Text = it.cos_sec;
            AssyComp.Text = it.Assy_Comp;
            CabNo.Text = it.cab_no;
            BinNo.Text = it.bin_number;
            OldPgRef.Text = it.old_pg_ref.ToString();
            ItemGroup.Text = it.group;
            ReOrdLvl.Text = it.Re_ord_lvl.ToString();
            SafetyStock.Text = it.safety_stk.ToString();
            SclAuth.Text = it.scl_auth.ToString();
            RepStock.Text = it.rep_stock.ToString();
            Remarks.Text = it.rmks;
        }

        // ✅ Update logic with safe conversions and backend integration
        private async void Update_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                // Parse numeric safely
                int.TryParse(SclAuth.Text, out int sclAuthValue);
                int.TryParse(ReOrdLvl.Text, out int reordValue);
                int.TryParse(SafetyStock.Text, out int safetyValue);
                int.TryParse(RepStock.Text, out int repValue);
                double.TryParse(OldPgRef.Text, out double oldPgValue);

                // Build updated LedgerItem
                var updated = new LedgerItem
                {
                    ledger_page = LedgerPage.Text,
                    ohs_number = OHSNo.Text,
                    isg_number = ISGNo.Text,
                    ssg_number = SSGNo.Text,
                    part_number = PartNo.Text,
                    nomenclature = Nomen.Text,
                    a_u = AU.Text,
                    scl_auth = sclAuthValue,
                    rep_stock = repValue,
                    cos_sec = COSSec.Text,
                    Assy_Comp = AssyComp.Text,
                    cab_no = CabNo.Text,
                    bin_number = BinNo.Text,
                    old_pg_ref = oldPgValue,
                    group = ItemGroup.Text,
                    Re_ord_lvl = reordValue,
                    safety_stk = safetyValue,
                    rmks = Remarks.Text,
                    Store = _item.Store,
                    SubStore = _item.SubStore
                };

                await ApiService.UpdateLedgerAsync(updated.ledger_page, updated);
                MessageBox.Show("✅ Ledger updated successfully!", "Success", MessageBoxButton.OK);
                DialogResult = true;
                Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"❌ Update failed: {ex.Message}");
            }
        }

        // ✅ Optional: Close page logic if implemented on backend
        private void ClosePage_Click(object sender, RoutedEventArgs e)
        {
            try
            {

                Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show($"❌ Failed to close page: {ex.Message}");
            }
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }
    }
}
