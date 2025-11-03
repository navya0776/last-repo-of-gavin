public class LedgerEntry
{
    public string LedgerPage { get; set; }
    public string OHSNo { get; set; }
    public string ISGNo { get; set; }
    public string SSGNo { get; set; }
    public string PartNo { get; set; }
    public string Nomen { get; set; }
    public string AU { get; set; }
    public string NoOff { get; set; }

    // Add missing properties to fix CS0117 errors
    public string DemandType { get; set; }
    public int Quantity { get; set; }
}