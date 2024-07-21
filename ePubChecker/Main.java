import javax.swing.JFrame;
import java.awt.Container;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.JTextField;
import javax.swing.JOptionPane;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;


import javax.xml.parsers.SAXParserFactory;
import javax.xml.parsers.SAXParser;
import org.xml.sax.helpers.DefaultHandler;
import org.xml.sax.SAXParseException;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.file.LinkOption;

import java.util.zip.ZipInputStream;
import java.util.zip.ZipEntry;

import java.io.ByteArrayInputStream;

import java.util.List;
import java.util.ArrayList;


import java.io.PrintWriter;


class Main {
    public static void main(String[] args) throws Exception {


        JFrame frame = new JFrame();
        frame.setTitle("電子書籍(ePub)ファイル内の(X)HTMLファイルのエラーチェック"); //ウィンドウのタイトルバーのタイトル
        frame.setSize(800, 300); //初期表示のウィンドウの横幅と高さ
        frame.setLocationRelativeTo(null); //モニターの中央に表示
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //ウィンドウ右上のXボタンで終了
        Container container = frame.getContentPane();
        container.setLayout(null); //LayoutManagerを使わず座標を指定して自由に配置

        JLabel epubLabel = new JLabel("");
        epubLabel.setSize(10, 10);
        epubLabel.setLocation(10, 40); //座標を指定
        container.add(epubLabel);

        JButton epubSelectButton = new JButton("電子書籍(ePub)ファイル選択");
        epubSelectButton.setSize(480, 20);
        epubSelectButton.setLocation(10, 10); //座標を指定
        container.add(epubSelectButton);

        //読み込みディレクトリ選択ボタンが押された時の処理
        epubSelectButton.addActionListener(
            actionEvent -> {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setFileFilter(new FileNameExtensionFilter("*.epub", "epub"));
                if (fileChooser.showOpenDialog(container) == JFileChooser.APPROVE_OPTION) {
                    epubLabel.setText(fileChooser.getSelectedFile().getAbsolutePath());
                    epubLabel.setSize(epubLabel.getText().length() * 20, 10);
                }
            }
        );

        JLabel outDirLabel = new JLabel("");
        outDirLabel.setSize(10, 10);
        outDirLabel.setLocation(10, 90); //座標を指定
        container.add(outDirLabel);

        JButton outDirSelectButton = new JButton("エラーチェック結果テキストファイル書き込みディレクトリ選択");
        outDirSelectButton.setSize(480, 20);
        outDirSelectButton.setLocation(10, 60); //座標を指定
        container.add(outDirSelectButton);

        //書き込みディレクトリ選択ボタンが押された時の処理
        outDirSelectButton.addActionListener(
            actionEvent -> {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setFileSelectionMode(JFileChooser.DIRECTORIES_ONLY);
                if (fileChooser.showOpenDialog(container) == JFileChooser.APPROVE_OPTION) {
                    outDirLabel.setText(fileChooser.getSelectedFile().getAbsolutePath());
                    outDirLabel.setSize(outDirLabel.getText().length() * 20, 10);
                }
            }
        );


        JButton checkEPubButton = new JButton("電子書籍(ePub)ファイル内の(X)HTMLファイルのエラーチェック");
        checkEPubButton.setSize(480, 20);
        checkEPubButton.setLocation(10, 140); //座標を指定
        container.add(checkEPubButton);

        //電子書籍(ePub)作成ボタンが押された時の処理
        checkEPubButton.addActionListener(actionEvent -> {
            try {

                String epub = epubLabel.getText();
                String outDir = outDirLabel.getText();

                if (epub.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "電子書籍(ePub)ファイルを選択してください。");
                    return;
                }

                if (outDir.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "エラーチェック結果テキストファイル書き込みディレクトリを選択してください。");
                    return;
                }

                if (Files.exists(Paths.get(epub)) == false) {
                    JOptionPane.showMessageDialog(frame, "電子書籍(ePub)ファイルを選択し直してください。");
                    return;
                }

                if (Files.exists(Paths.get(outDir)) == false) {
                    JOptionPane.showMessageDialog(frame, "エラーチェック結果テキストファイル書き込みディレクトリを選択し直してください。");
                    return;
                }

                String epubCheckDateTime = ZonedDateTime.now().format(DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss.SSS"));

                List<String> warningMessageList = new ArrayList<>();
                List<String> errorMessageList = new ArrayList<>();


                SAXParserFactory saxParserFactory = SAXParserFactory.newInstance();
                SAXParser saxParser = saxParserFactory.newSAXParser();


                Path epubFilePath = Paths.get(epub);

                try (ZipInputStream zipInputStream = new ZipInputStream(Files.newInputStream(epubFilePath))) {
                    for (ZipEntry zipEntry = zipInputStream.getNextEntry(); zipEntry != null; zipEntry = zipInputStream.getNextEntry()) {

                        String fileName = zipEntry.getName();

                        if (fileName.matches(".+\\.xhtml|.+\\.html?") == false) {
                            continue;
                        }


                        DefaultHandler defaultHandler = new DefaultHandler() {
                            public void warning(SAXParseException saxParseException) {
                                warningMessageList.add("警告: " + fileName + ": 第" + saxParseException.getLineNumber() + "行: " + saxParseException.getMessage());
                            }
                            public void error(SAXParseException saxParseException) {
                                errorMessageList.add("エラー: " + fileName + ": 第" + saxParseException.getLineNumber() + "行: " + saxParseException.getMessage());
                            }
                            public void fatalError(SAXParseException saxParseException) {
                                errorMessageList.add("致命的なエラー: " + fileName + ": 第" + saxParseException.getLineNumber() + "行: " + saxParseException.getMessage());
                            }
                        };


                        try {
                            saxParser.parse(new ByteArrayInputStream(zipInputStream.readAllBytes()), defaultHandler);

                        } catch (SAXParseException saxParseException) {
                            //SAXParseExceptionを無視
                        }

                        zipInputStream.closeEntry();
                    }
                }


                String checkResultTextFilePathString = outDir + "/電子書籍チェック結果" + epubCheckDateTime + ".txt";

                Path checkResultTextFilePath = Paths.get(checkResultTextFilePathString);

                try (PrintWriter printWriter = new PrintWriter(Files.newBufferedWriter(checkResultTextFilePath))) {

                    if (1 <= errorMessageList.size()) {
                        printWriter.print(epub + "内の(X)HTMLファイルにはエラーが有ります。\n");
                        printWriter.print(String.join("\n", errorMessageList) + "\n");
                    } else {
                        printWriter.print(epub + "内の(X)HTMLファイルにはエラーが無いようです。\n");
                    }

                    if (1 <= warningMessageList.size()) {
                        printWriter.print(String.join("\n", warningMessageList) + "\n");
                    }


                    if (1 <= errorMessageList.size()) {
                        JOptionPane.showMessageDialog(frame, epub + "内の(X)HTMLファイルにはエラーが有ります。");
                    } else {
                        JOptionPane.showMessageDialog(frame, epub + "内の(X)HTMLファイルにはエラーが無いようです。");
                    }
                }


            } catch (Exception exception) {
                JOptionPane.showMessageDialog(frame, "エラー: " + exception);
                throw new RuntimeException(exception);
            }
        });

        frame.setVisible(true); //ウィンドウを表示
    }
}
