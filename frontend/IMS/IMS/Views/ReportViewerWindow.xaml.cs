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

            // ================= PAGE SETUP =================
            var sectionProps = new SectionProperties(
                new PageSize
                {
                    Width = 12240,   // A4
                    Height = 15840,
                    Orient = PageOrientationValues.Portrait
                },
                new PageMargin
                {
                    Top = 720,
                    Bottom = 720,
                    Left = 720,
                    Right = 720
                }
            );

            // ================= HEADER =================
            var headerPart = mainPart.AddNewPart<HeaderPart>();
            headerPart.Header = new Header(
                new Paragraph(
                    new ParagraphProperties(
                        new Justification { Val = JustificationValues.Center }
                    ),
                    new Run(
                        new RunProperties(new Bold()),
                        new Text("IMS REPORT")
                    )
                )
            );

            sectionProps.Append(new HeaderReference
            {
                Type = HeaderFooterValues.Default,
                Id = mainPart.GetIdOfPart(headerPart)
            });

            // ================= FOOTER =================
            var footerPart = mainPart.AddNewPart<FooterPart>();
            footerPart.Footer = new Footer(
                new Paragraph(
                    new ParagraphProperties(
                        new Justification { Val = JustificationValues.Center }
                    ),
                    new Run(new Text($"Generated on {DateTime.Now:dd-MMM-yyyy}"))
                )
            );

            sectionProps.Append(new FooterReference
            {
                Type = HeaderFooterValues.Default,
                Id = mainPart.GetIdOfPart(footerPart)
            });

            // ================= TITLE =================
            var titlePara = new Paragraph(
                new ParagraphProperties(
                    new Justification { Val = JustificationValues.Center },
                    new SpacingBetweenLines { After = "400" }
                ),
                new Run(
                    new RunProperties(
                        new Bold(),
                        new FontSize { Val = "36" } // 18pt
                    ),
                    new Text(TitleBlock.Text)
                )
            );
            body.Append(titlePara);

            // ================= TABLE =================
            var table = new Table();

            table.AppendChild(new TableProperties(
                new TableWidth { Width = "5000", Type = TableWidthUnitValues.Pct },
                new TableBorders(
                    new TopBorder { Val = BorderValues.Single, Size = 6 },
                    new BottomBorder { Val = BorderValues.Single, Size = 6 },
                    new LeftBorder { Val = BorderValues.Single, Size = 6 },
                    new RightBorder { Val = BorderValues.Single, Size = 6 },
                    new InsideHorizontalBorder { Val = BorderValues.Single, Size = 6 },
                    new InsideVerticalBorder { Val = BorderValues.Single, Size = 6 }
                )
            ));

            // ---------- HEADER ROW ----------
            var headerRow = new TableRow();
            foreach (var col in ReportGrid.Columns)
            {
                headerRow.Append(
                    new TableCell(
                        new Paragraph(
                            new ParagraphProperties(
                                new Justification { Val = JustificationValues.Center }
                            ),
                            new Run(
                                new RunProperties(new Bold()),
                                new Text(col.Header?.ToString() ?? "")
                            )
                        )
                    )
                );
            }
            table.Append(headerRow);

            // ---------- DATA ROWS ----------
            foreach (var item in ReportGrid.Items)
            {
                if (item == CollectionView.NewItemPlaceholder) continue;

                var row = new TableRow();

                foreach (var col in ReportGrid.Columns)
                {
                    string value = "";
                    if (col.GetCellContent(item) is TextBlock tb)
                        value = tb.Text;

                    row.Append(
                        new TableCell(
                            new Paragraph(
                                new ParagraphProperties(
                                    new Justification { Val = JustificationValues.Left }
                                ),
                                new Run(new Text(value))
                            )
                        )
                    );
                }
                table.Append(row);
            }

            body.Append(table);
            body.Append(sectionProps);
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
