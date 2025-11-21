using System;
using System.Windows;

namespace IMS.Windows
{
    public partial class RangeWindow : Window
    {
        // Public properties the caller reads after ShowDialog()
        public int FromValue { get; private set; }
        public int ToValue { get; private set; }

        public RangeWindow()
        {
            InitializeComponent();
        }

        private void Cancel_Click(object sender, RoutedEventArgs e)
        {
            DialogResult = false;
            Close();
        }

        private void Add_Click(object sender, RoutedEventArgs e)
        {
            // Validate numeric input and logical order
            if (!int.TryParse(FromTextBox.Text.Trim(), out int from))
            {
                MessageBox.Show("Please enter a valid integer for From.", "Invalid Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                FromTextBox.Focus();
                return;
            }

            if (!int.TryParse(ToTextBox.Text.Trim(), out int to))
            {
                MessageBox.Show("Please enter a valid integer for To.", "Invalid Input", MessageBoxButton.OK, MessageBoxImage.Warning);
                ToTextBox.Focus();
                return;
            }

            if (from > to)
            {
                MessageBox.Show("'From' must be less than or equal to 'To'.", "Invalid Range", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            FromValue = from;
            ToValue = to;

            DialogResult = true;
            Close();
        }
    }
}
