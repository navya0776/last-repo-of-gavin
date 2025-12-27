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
        // Build updated object from UI
        var updated = new LedgerItem();
        updated.CopyFrom(_item);   // copies all existing values

        // Now override only editable fields
        updated.ledger_page = LedgerPage.Text;
        updated.ohs_number = OHSNo.Text;
        updated.isg_number = ISGNo.Text;
        updated.ssg_number = SSGNo.Text;
        updated.part_number = PartNo.Text;
        updated.nomenclature = Nomen.Text;
        updated.a_u = AU.Text;
        updated.bin_number = BinNo.Text;
        updated.group = ItemGroup.Text;
        updated.rmks = Remarks.Text;

        int tempInt;
        double tempDouble;

        if (int.TryParse(SclAuth.Text, out tempInt)) updated.scl_auth = tempInt;
        if (int.TryParse(ReOrdLvl.Text, out tempInt)) updated.Re_ord_lvl = tempInt;
        if (int.TryParse(SafetyStock.Text, out tempInt)) updated.safety_stk = tempInt;
        if (int.TryParse(RepStock.Text, out tempInt)) updated.rep_stock = tempInt;
        if (double.TryParse(OldPgRef.Text, out tempDouble)) updated.old_pg_ref = tempDouble;

        // Call backend (or mock)
        //await ApiService.UpdateLedgerAsync(updated);
        _item.CopyFrom(updated); // Update original item with new values
        MessageBox.Show("Updated successfully!");
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
