using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel;
using System.IO;
using System.Linq;
using System.Printing;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;

using DocumentFormat.OpenXml;
using DocumentFormat.OpenXml.Packaging;
using DocumentFormat.OpenXml.Wordprocessing;

using WordParagraph = DocumentFormat.OpenXml.Wordprocessing.Paragraph;
using WordRun = DocumentFormat.OpenXml.Wordprocessing.Run;
using WordText = DocumentFormat.OpenXml.Wordprocessing.Text;
using WordTable = DocumentFormat.OpenXml.Wordprocessing.Table;
using WordRow = DocumentFormat.OpenXml.Wordprocessing.TableRow;
using WordCell = DocumentFormat.OpenXml.Wordprocessing.TableCell;

namespace IMS.Views
{
    public partial class ReportViewerWindow : Window
    {
        private readonly IEnumerable _originalItems;
        private readonly ICollectionView _view;

        public ReportViewerWindow(string title, IEnumerable items)
        {
            InitializeComponent();

            TitleBlock.Text = title;

            _originalItems = items ?? Array.Empty<object>();
            _view = CollectionViewSource.GetDefaultView(_originalItems);

            ReportGrid.ItemsSource = _view;
        }

        // Global helper for opening the window
        public static void ShowReport(string title, IEnumerable rows)
        {
            var win = new ReportViewerWindow(title, rows);
            win.Owner = Application.Current.MainWindow;
            win.ShowDialog();
        }

        // Close
        private void CloseButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        // Search
        private void SearchBox_TextChanged(object sender, TextChangedEventArgs e)
        {
            if (_view == null) return;

            string text = SearchBox.Text?.Trim() ?? "";

            if (string.IsNullOrEmpty(text))
            {
                _view.Filter = null;
            }
            else
            {
                _view.Filter = obj =>
                {
                    if (obj == null) return false;

                    var props = TypeDescriptor.GetProperties(obj)
                                              .Cast<PropertyDescriptor>();

                    string combined = string.Join(" ",
                        props.Select(p => p.GetValue(obj)?.ToString() ?? ""));

                    return combined.IndexOf(text, StringComparison.OrdinalIgnoreCase) >= 0;
                };
            }

            _view.Refresh();
        }

        // ==== EXPORT WORD ====
        private void ExportWord_Click(object sender, RoutedEventArgs e)
        {
            var dialog = new Microsoft.Win32.SaveFileDialog
            {
                Filter = "Word Document (*.docx)|*.docx",
                FileName = $"{TitleBlock.Text}.docx"
            };

            if (dialog.ShowDialog() == true)
            {
                ExportToWord(dialog.FileName);
                MessageBox.Show("Exported to Word");
            }
        }

        private void ExportToWord(string path)
        {
            using var doc = WordprocessingDocument.Create(path, WordprocessingDocumentType.Document);
            var mainPart = doc.AddMainDocumentPart();

            mainPart.Document = new Document();
            var body = mainPart.Document.AppendChild(new Body());

            var titlePara = new WordParagraph(
                new Run(new Text(TitleBlock.Text))
            );
            body.Append(titlePara);

            var table = new WordTable();

            // Header
            var header = new WordRow();
            foreach (var col in ReportGrid.Columns)
            {
                header.Append(new WordCell(new WordParagraph(new WordRun(new WordText(col.Header?.ToString())))));
            }
            table.Append(header);

            // Rows
            foreach (var item in ReportGrid.Items)
            {
                if (item == CollectionView.NewItemPlaceholder) continue;

                var row = new WordRow();

                foreach (var col in ReportGrid.Columns)
                {
                    string val = "";
                    if (col.GetCellContent(item) is TextBlock tb) val = tb.Text;

                    row.Append(new WordCell(new WordParagraph(new WordRun(new WordText(val)))));
                }

                table.Append(row);
            }

            body.Append(table);
        }

        // ==== EXPORT CSV ====
        private void ExportExcel_Click(object sender, RoutedEventArgs e)
        {
            var dlg = new Microsoft.Win32.SaveFileDialog
            {
                Filter = "CSV Files (*.csv)|*.csv",
                FileName = $"{TitleBlock.Text}.csv"
            };

            if (dlg.ShowDialog() == true)
            {
                using var writer = new StreamWriter(dlg.FileName);

                // Header
                writer.WriteLine(string.Join(",", ReportGrid.Columns.Select(c => c.Header)));

                // Rows
                foreach (var item in ReportGrid.Items)
                {
                    if (item == CollectionView.NewItemPlaceholder) continue;

                    var cells = new List<string>();
                    foreach (var col in ReportGrid.Columns)
                    {
                        if (col.GetCellContent(item) is TextBlock tb)
                            cells.Add(tb.Text);
                        else
                            cells.Add("");
                    }

                    writer.WriteLine(string.Join(",", cells));
                }

                MessageBox.Show("Exported to CSV");
            }
        }

        // ==== PRINT ====
        private void Print_Click(object sender, RoutedEventArgs e)
        {
            var dlg = new PrintDialog();

            if (dlg.ShowDialog() == true)
            {
                dlg.PrintVisual(ReportGrid, TitleBlock.Text);
            }
        }
    }
}
