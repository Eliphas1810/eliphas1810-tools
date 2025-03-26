import javax.swing.JFrame;
import java.awt.Container;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.JTextField;
import javax.swing.JOptionPane;
import javax.swing.ImageIcon;

import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.Files;
import java.nio.file.StandardOpenOption;

import java.nio.charset.Charset;
import java.nio.charset.StandardCharsets;

import java.util.ArrayList;
import java.util.Arrays;

import java.io.BufferedOutputStream;

public class Main {

    private static String imageMimetype = null;
    private static ArrayList<Byte> imageByteList = new ArrayList<>();
    private static ArrayList<Byte> mpegFrameByteList = new ArrayList<>();

    public static void main(String[] args) throws Exception {
        JFrame frame = new JFrame();
        frame.setTitle("MP3のID3v2タグ編集"); //ウィンドウのタイトルバーのタイトル
        frame.setSize(800, 600); //初期表示のウィンドウの横幅と高さ
        frame.setLocationRelativeTo(null); //モニターの中央に表示
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //ウィンドウ右上のXボタンで終了

        Container container = frame.getContentPane();
        container.setLayout(null); //LayoutManagerを使わず座標を指定して自由に配置

        JLabel mp3Label = new JLabel("");
        mp3Label.setSize(10, 10);
        mp3Label.setLocation(10, 40); //座標を指定
        container.add(mp3Label);

        JButton mp3SelectButton = new JButton("MP3ファイル選択");
        mp3SelectButton.setSize(240, 20);
        mp3SelectButton.setLocation(10, 10); //座標を指定
        container.add(mp3SelectButton);

        JLabel titleLabel = new JLabel("曲名");
        titleLabel.setSize(100, 10);
        titleLabel.setLocation(10, 60); //座標を指定
        container.add(titleLabel);

        JTextField titleTextField = new JTextField(80);
        titleTextField.setSize(640, 20);
        titleTextField.setLocation(110, 60); //座標を指定
        container.add(titleTextField);

        JLabel artistLabel = new JLabel("アーティスト名");
        artistLabel.setSize(100, 10);
        artistLabel.setLocation(10, 90); //座標を指定
        container.add(artistLabel);

        JTextField artistTextField = new JTextField(80);
        artistTextField.setSize(640, 20);
        artistTextField.setLocation(110, 90); //座標を指定
        container.add(artistTextField);

        JLabel albumLabel = new JLabel("アルバム名");
        albumLabel.setSize(100, 10);
        albumLabel.setLocation(10, 120); //座標を指定
        container.add(albumLabel);

        JTextField albumTextField = new JTextField(80);
        albumTextField.setSize(640, 20);
        albumTextField.setLocation(110, 120); //座標を指定
        container.add(albumTextField);

        JLabel trackLabel = new JLabel("トラック番号");
        trackLabel.setSize(100, 10);
        trackLabel.setLocation(10, 150); //座標を指定
        container.add(trackLabel);

        JTextField trackTextField = new JTextField(80);
        trackTextField.setSize(640, 20);
        trackTextField.setLocation(110, 150); //座標を指定
        container.add(trackTextField);

        JButton makeMp3Button = new JButton("新MP3ファイル作成");
        makeMp3Button.setSize(240, 20);
        makeMp3Button.setLocation(10, 180); //座標を指定
        container.add(makeMp3Button);

        JLabel imageLabel = new JLabel("画像 無し");
        imageLabel.setSize(700, 300);
        imageLabel.setLocation(10, 210); //座標を指定
        container.add(imageLabel);

        JButton imageSelectButton = new JButton("画像ファイル選択");
        imageSelectButton.setSize(240, 20);
        imageSelectButton.setLocation(10, 530); //座標を指定
        container.add(imageSelectButton);


        //MP3ファイル選択ボタンが押された時の処理
        mp3SelectButton.addActionListener(
            actionEvent -> {
                try {
                    JFileChooser fileChooser = new JFileChooser();
                    fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                    fileChooser.setFileFilter(new FileNameExtensionFilter("MP3", "mp3"));
                    if (fileChooser.showOpenDialog(container) == JFileChooser.APPROVE_OPTION) {

                        if (fileChooser.getSelectedFile().getAbsolutePath().matches("^.+\\.[mM][pP]3$") == false) {
                            JOptionPane.showMessageDialog(frame, "MP3ファイルを選択してください。");
                            return;
                        }

                        mp3Label.setText(fileChooser.getSelectedFile().getAbsolutePath());
                        mp3Label.setSize(mp3Label.getText().length() * 20, 10);

                        byte[] byteArray = Files.readAllBytes(fileChooser.getSelectedFile().toPath());

                        titleTextField.setText("");
                        artistTextField.setText("");
                        albumTextField.setText("");
                        trackTextField.setText("");

                        imageLabel.setText("画像 無し");
                        imageLabel.setIcon(null);

                        imageMimetype = null;
                        imageByteList.clear();
                        mpegFrameByteList.clear();

                        String id3 = new String(Arrays.copyOfRange(byteArray, 0, 3), StandardCharsets.UTF_8);
                        if (id3.equals("ID3") == false) {
                            //ID3v2タグが無い場合
                            for (int index = 0; index < byteArray.length; index++) {
                                mpegFrameByteList.add(byteArray[index]);
                            }
                            return;
                        }

                        int minorVersion = Byte.toUnsignedInt(byteArray[3]);
                        if (minorVersion <= 2 || 5 <= minorVersion) {
                            JOptionPane.showMessageDialog(frame, "当アプリケーションはID3v2.3とID3v2.4以外には未対応です。\n他のアプリケーションを利用してください。");
                            return;
                        }

                        //int batchVersion = Byte.toUnsignedInt(byteArray[4]);

                        byte flag = byteArray[5];
                        boolean hasExHeader = ((flag & 0x02) != 0);
                        int headerSize = 0;
                        headerSize += (Byte.toUnsignedInt(byteArray[6]) << 21);
                        headerSize += (Byte.toUnsignedInt(byteArray[7]) << 14);
                        headerSize += (Byte.toUnsignedInt(byteArray[8]) << 7);
                        headerSize += Byte.toUnsignedInt(byteArray[9]);

                        int byteIndex = 10;

                        if (hasExHeader) {
                            int exHeaderSize = 0;
                            if (minorVersion == 3) {
                                exHeaderSize += (Byte.toUnsignedInt(byteArray[10]) << 24);
                                exHeaderSize += (Byte.toUnsignedInt(byteArray[11]) << 16);
                                exHeaderSize += (Byte.toUnsignedInt(byteArray[12]) << 8);
                                exHeaderSize += Byte.toUnsignedInt(byteArray[13]);
                            } else {
                                exHeaderSize += (Byte.toUnsignedInt(byteArray[10]) << 21);
                                exHeaderSize += (Byte.toUnsignedInt(byteArray[11]) << 14);
                                exHeaderSize += (Byte.toUnsignedInt(byteArray[12]) << 7);
                                exHeaderSize += Byte.toUnsignedInt(byteArray[13]);
                            }
                            byteIndex += exHeaderSize;
                        }

                        while (byteIndex < headerSize) {

                            String frameId = new String(Arrays.copyOfRange(byteArray, byteIndex, byteIndex + 4), StandardCharsets.UTF_8);
                            byteIndex += 4;

                            if (byteIndex == 14 && frameId.matches("^[A-Z][A-Z][A-Z][A-Z0-9]$") == false) {
                                byteIndex -= 4;
                                int exHeaderSize = 0;
                                if (minorVersion == 3) {
                                    exHeaderSize += (Byte.toUnsignedInt(byteArray[10]) << 24);
                                    exHeaderSize += (Byte.toUnsignedInt(byteArray[11]) << 16);
                                    exHeaderSize += (Byte.toUnsignedInt(byteArray[12]) << 8);
                                    exHeaderSize += Byte.toUnsignedInt(byteArray[13]);
                                } else {
                                    exHeaderSize += (Byte.toUnsignedInt(byteArray[10]) << 21);
                                    exHeaderSize += (Byte.toUnsignedInt(byteArray[11]) << 14);
                                    exHeaderSize += (Byte.toUnsignedInt(byteArray[12]) << 7);
                                    exHeaderSize += Byte.toUnsignedInt(byteArray[13]);
                                }
                                byteIndex += exHeaderSize;
                                continue;
                            }


                            int frameSize = 0;
                            if (minorVersion == 3) {
                                frameSize += (Byte.toUnsignedInt(byteArray[byteIndex]) << 24);
                                frameSize += (Byte.toUnsignedInt(byteArray[byteIndex + 1]) << 16);
                                frameSize += (Byte.toUnsignedInt(byteArray[byteIndex + 2]) << 8);
                                frameSize += Byte.toUnsignedInt(byteArray[byteIndex + 3]);
                            } else {
                                frameSize += (Byte.toUnsignedInt(byteArray[byteIndex]) << 21);
                                frameSize += (Byte.toUnsignedInt(byteArray[byteIndex + 1]) << 14);
                                frameSize += (Byte.toUnsignedInt(byteArray[byteIndex + 2]) << 7);
                                frameSize += Byte.toUnsignedInt(byteArray[byteIndex + 3]);
                            }
                            byteIndex += 4;

                            byteIndex += 2; //フレームのフラグは無視して飛ばします。

                            if (frameId.matches("^TIT2$|^TPE1$|^TALB$|^TRCK$")) {

                                byte encodingByte = byteArray[byteIndex];
                                Charset charset = null;
                                if (encodingByte == 0x00) {
                                    //charset = Charset.forName("ISO-8859-1");
                                    charset = Charset.forName("Windows-31J"); //過去の日本語のアプリケーションにはISO-8859-1でWindowsの日本語のテキストを書き込んでいた物が有ったそうです。
                                } else if (encodingByte == 0x01) {
                                    charset = Charset.forName("UTF-16");
                                } else if (minorVersion == 4 && encodingByte == 0x02) {
                                    charset = Charset.forName("UTF-16BE");
                                } else if (minorVersion == 4 && encodingByte == 0x03) {
                                    charset = Charset.forName("utf-8");
                                } else {
                                    throw new Exception("存在しないID3v2マイナーバージョンとテキスト エンコーディングの16進数表記の組み合わせです。");
                                }
                                byteIndex += 1;

                                String content = "";

                                ArrayList<Byte> contentByteList = new ArrayList<>();
                                for (int index = 0; index < frameSize - 1; index++) {
                                    contentByteList.add(byteArray[byteIndex + index]);
                                }
                                byteIndex += contentByteList.size();
                                byte[] contentByteArray = new byte[contentByteList.size()];
                                for (int index = 0; index < contentByteArray.length; index++) {
                                    contentByteArray[index] = contentByteList.get(index);
                                }
                                content = new String(contentByteArray, charset);

                                if (frameId.equals("TIT2")) {
                                    titleTextField.setText(content);
                                } else if (frameId.equals("TPE1")) {
                                    artistTextField.setText(content);
                                } else if (frameId.equals("TALB")) {
                                    albumTextField.setText(content);
                                } else if (frameId.equals("TRCK")) {
                                    trackTextField.setText(content);
                                }

                            } else if (frameId.equals("APIC")) {

                                byte encodingByte = byteArray[byteIndex];
                                Charset charset = null;
                                if (encodingByte == 0x00) {
                                    //charset = Charset.forName("ISO-8859-1");
                                    charset = Charset.forName("Windows-31J"); //過去の日本語のアプリケーションにはISO-8859-1でWindowsの日本語のテキストを書き込んでいた物が有ったそうです。
                                } else if (encodingByte == 0x01) {
                                    charset = Charset.forName("UTF-16");
                                } else if (minorVersion == 4 && encodingByte == 0x02) {
                                    charset = Charset.forName("UTF-16BE");
                                } else if (minorVersion == 4 && encodingByte == 0x03) {
                                    charset = Charset.forName("utf-8");
                                } else {
                                    throw new Exception("存在しないID3v2マイナーバージョンとテキスト エンコーディングの16進数表記の組み合わせです。");
                                }
                                byteIndex += 1;

                                ArrayList<Byte> mimetypeByteList = new ArrayList<>();
                                for (int index = 0; index < frameSize - 1; index++) {
                                    byte currentByte = byteArray[byteIndex + index];
                                    if (currentByte == 0x00/* NULL */) {
                                        break;
                                    }
                                    mimetypeByteList.add(currentByte);
                                }
                                byte[] mimetypeByteArray = new byte[mimetypeByteList.size()];
                                for (int index = 0; index < mimetypeByteArray.length; index++) {
                                    mimetypeByteArray[index] = mimetypeByteList.get(index);
                                }
                                imageMimetype = new String(mimetypeByteArray, charset);
                                byteIndex += (mimetypeByteList.size() + 1);

                                byteIndex += 1; //Picture Type(画像の種類)を無視して飛ばします。

                                ArrayList<Byte> descriptionList = new ArrayList<>();
                                for (int index = 0; index < (frameSize - 1 - mimetypeByteList.size() - 1 - 1); index++) {
                                    byte currentByte = byteArray[byteIndex + index];
                                    if (currentByte == 0x00/* NULL */) {
                                        break;
                                    }
                                    descriptionList.add(currentByte);
                                }
                                byteIndex += (descriptionList.size() + 1);

                                for (int index = 0; index < (frameSize - 1 - mimetypeByteList.size() - 1 - 1 - descriptionList.size() - 1); index++) {
                                    imageByteList.add(byteArray[byteIndex + index]);
                                }
                                byte[] imageByteArray = new byte[imageByteList.size()];
                                for (int index = 0; index < imageByteArray.length; index++) {
                                    imageByteArray[index] = imageByteList.get(index);
                                }
                                imageLabel.setText("");
                                imageLabel.setIcon(new ImageIcon(imageByteArray));

                            } else {
                                byteIndex += frameSize;
                            }
                        }

                        if (headerSize < byteIndex) {
                            byteIndex = headerSize;
                        }

                        for (; byteIndex < byteArray.length; byteIndex++) {
                            mpegFrameByteList.add(byteArray[byteIndex]);
                        }
                    }
                } catch (Exception exception) {
                    JOptionPane.showMessageDialog(frame, "エラー: " + exception);
                    throw new RuntimeException(exception);
                }
            }
        );


        //画像ファイル選択ボタンが押された時の処理
        imageSelectButton.addActionListener(
            actionEvent -> {
                try {
                    JFileChooser fileChooser = new JFileChooser();
                    fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                    fileChooser.setFileFilter(new FileNameExtensionFilter("PNG or JPEG Image", "png", "jpg", "jpeg"));
                    if (fileChooser.showOpenDialog(container) == JFileChooser.APPROVE_OPTION) {

                        if (fileChooser.getSelectedFile().getAbsolutePath().matches("^.+\\.[pP][nN][gG]$|^.+\\.[jJ][pP][eE]?[gG]$") == false) {
                            JOptionPane.showMessageDialog(frame, "PNG形式かJPEG形式の画像ファイルを選択してください。");
                            return;
                        }

                        byte[] byteArray = Files.readAllBytes(fileChooser.getSelectedFile().toPath());

                        imageLabel.setText("");

                        if (fileChooser.getSelectedFile().getAbsolutePath().matches("^.+\\.[pP][nN][gG]$")) {
                            imageMimetype = "image/png";
                        } else {
                            imageMimetype = "image/jpeg";
                        }

                        imageByteList.clear();
                        for (int index = 0; index < byteArray.length; index++) {
                            imageByteList.add(byteArray[index]);
                        }
                        byte[] imageByteArray = new byte[imageByteList.size()];
                        for (int index = 0; index < imageByteArray.length; index++) {
                            imageByteArray[index] = imageByteList.get(index);
                        }
                        imageLabel.setIcon(new ImageIcon(imageByteArray));
                    }
                } catch (Exception exception) {
                    JOptionPane.showMessageDialog(frame, "エラー: " + exception);
                    throw new RuntimeException(exception);
                }
            }
        );


        //新MP3作成ボタンが押された時の処理
        makeMp3Button.addActionListener(actionEvent -> {
            try {

                if (mpegFrameByteList.size() <= 0) {
                    JOptionPane.showMessageDialog(frame, "MP3ファイルを選択してください。");
                    return;
                }

                String title = titleTextField.getText();
                String artist = artistTextField.getText();
                String album = albumTextField.getText();
                String track = trackTextField.getText();

                if (title.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "曲名を記入してください。");
                    return;
                }
                if (artist.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "アーティスト名を記入してください。");
                    return;
                }
                if (track.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "トラック番号を記入してください。");
                    return;
                }

                String mp3FilePath = mp3Label.getText();

                Path mp3DirPath = Paths.get(mp3FilePath).getParent();

                Path newMp3FilePath = mp3DirPath.resolve(title + ".mp3");

                byte[] titleByteArray = title.getBytes(StandardCharsets.UTF_8);
                byte[] artistByteArray = artist.getBytes(StandardCharsets.UTF_8);
                byte[] albumByteArray = album.getBytes(StandardCharsets.UTF_8);
                byte[] trackByteArray = track.getBytes(StandardCharsets.UTF_8);

                int headerSize = 0;
                headerSize += 10;
                headerSize += (10 + 1 + titleByteArray.length);
                headerSize += (10 + 1 + artistByteArray.length);
                headerSize += (10 + 1 + trackByteArray.length);
                if (album.isEmpty() == false) {
                    headerSize += (10 + 1 + albumByteArray.length);
                }
                if (1 <= imageByteList.size()) {
                    headerSize += (10 + 1 + imageMimetype.length() + 1 + 1 + 1 + imageByteList.size());
                }

                int fileSize = headerSize + mpegFrameByteList.size();

                try(
                    BufferedOutputStream bufferedOutputStream = new BufferedOutputStream(Files.newOutputStream(newMp3FilePath, StandardOpenOption.WRITE, StandardOpenOption.CREATE, StandardOpenOption.TRUNCATE_EXISTING));
                ) {

                    //Javaはデフォルトはビッグ エンディアン
                    //ID3v2タグはビッグ エンディアン

                    bufferedOutputStream.write(0x49/* I */);
                    bufferedOutputStream.write(0x44/* D */);
                    bufferedOutputStream.write(0x33/* 3 */);
                    bufferedOutputStream.write(0x04/* マイナーバージョン4 */);
                    bufferedOutputStream.write(0x00/* パッチバージョン0 */);
                    bufferedOutputStream.write(0x00/* ヘッダーのフラグ */);
                    bufferedOutputStream.write(headerSize << 4 >>> 25);
                    bufferedOutputStream.write(headerSize << 11 >>> 25);
                    bufferedOutputStream.write(headerSize << 18 >>> 25);
                    bufferedOutputStream.write(headerSize << 25 >>> 25);

                    bufferedOutputStream.write(0x54/* T */);
                    bufferedOutputStream.write(0x49/* I */);
                    bufferedOutputStream.write(0x54/* T */);
                    bufferedOutputStream.write(0x32/* 2 */);
                    bufferedOutputStream.write((1 + titleByteArray.length) << 4 >>> 25);
                    bufferedOutputStream.write((1 + titleByteArray.length) << 11 >>> 25);
                    bufferedOutputStream.write((1 + titleByteArray.length) << 18 >>> 25);
                    bufferedOutputStream.write((1 + titleByteArray.length) << 25 >>> 25);
                    bufferedOutputStream.write(0x00/* フレームのフラグ */);
                    bufferedOutputStream.write(0x00/* フレームのフラグ */);
                    bufferedOutputStream.write(0x03/* テキストのフレームの文字コード。UTF-8は16進数で03。 */);
                    for (int index = 0; index < titleByteArray.length; index++) {
                        bufferedOutputStream.write(titleByteArray[index]);
                    }

                    bufferedOutputStream.write(0x54/* T */);
                    bufferedOutputStream.write(0x50/* P */);
                    bufferedOutputStream.write(0x45/* E */);
                    bufferedOutputStream.write(0x31/* 1 */);
                    bufferedOutputStream.write((1 + artistByteArray.length) << 4 >>> 25);
                    bufferedOutputStream.write((1 + artistByteArray.length) << 11 >>> 25);
                    bufferedOutputStream.write((1 + artistByteArray.length) << 18 >>> 25);
                    bufferedOutputStream.write((1 + artistByteArray.length) << 25 >>> 25);
                    bufferedOutputStream.write(0x00/* フレームのフラグ */);
                    bufferedOutputStream.write(0x00/* フレームのフラグ */);
                    bufferedOutputStream.write(0x03/* テキストのフレームの文字コード。UTF-8は16進数で03。 */);
                    for (int index = 0; index < artistByteArray.length; index++) {
                        bufferedOutputStream.write(artistByteArray[index]);
                    }

                    bufferedOutputStream.write(0x54/* T */);
                    bufferedOutputStream.write(0x52/* R */);
                    bufferedOutputStream.write(0x43/* C */);
                    bufferedOutputStream.write(0x4B/* K */);
                    bufferedOutputStream.write((1 + trackByteArray.length) << 4 >>> 25);
                    bufferedOutputStream.write((1 + trackByteArray.length) << 11 >>> 25);
                    bufferedOutputStream.write((1 + trackByteArray.length) << 18 >>> 25);
                    bufferedOutputStream.write((1 + trackByteArray.length) << 25 >>> 25);
                    bufferedOutputStream.write(0x00/* フレームのフラグ */);
                    bufferedOutputStream.write(0x00/* フレームのフラグ */);
                    bufferedOutputStream.write(0x03/* テキストのフレームの文字コード。UTF-8は16進数で03。 */);
                    for (int index = 0; index < trackByteArray.length; index++) {
                        bufferedOutputStream.write(trackByteArray[index]);
                    }

                    if (album.isEmpty() == false) {
                        bufferedOutputStream.write(0x54/* T */);
                        bufferedOutputStream.write(0x41/* A */);
                        bufferedOutputStream.write(0x4C/* L */);
                        bufferedOutputStream.write(0x42/* B */);
                        bufferedOutputStream.write((1 + albumByteArray.length) << 4 >>> 25);
                        bufferedOutputStream.write((1 + albumByteArray.length) << 11 >>> 25);
                        bufferedOutputStream.write((1 + albumByteArray.length) << 18 >>> 25);
                        bufferedOutputStream.write((1 + albumByteArray.length) << 25 >>> 25);
                        bufferedOutputStream.write(0x00/* フレームのフラグ */);
                        bufferedOutputStream.write(0x00/* フレームのフラグ */);
                        bufferedOutputStream.write(0x03/* テキストのフレームの文字コード。UTF-8は16進数で03。 */);
                        for (int index = 0; index < albumByteArray.length; index++) {
                            bufferedOutputStream.write(albumByteArray[index]);
                        }
                    }

                    if (1 <= imageByteList.size()) {
                        bufferedOutputStream.write(0x41/* A */);
                        bufferedOutputStream.write(0x50/* P */);
                        bufferedOutputStream.write(0x49/* I */);
                        bufferedOutputStream.write(0x43/* C */);
                        bufferedOutputStream.write((1 + imageMimetype.length() + 1 + 1 + 1 + imageByteList.size()) << 4 >>> 25);
                        bufferedOutputStream.write((1 + imageMimetype.length() + 1 + 1 + 1 + imageByteList.size()) << 11 >>> 25);
                        bufferedOutputStream.write((1 + imageMimetype.length() + 1 + 1 + 1 + imageByteList.size()) << 18 >>> 25);
                        bufferedOutputStream.write((1 + imageMimetype.length() + 1 + 1 + 1 + imageByteList.size()) << 25 >>> 25);
                        bufferedOutputStream.write(0x00/* フレームのフラグ */);
                        bufferedOutputStream.write(0x00/* フレームのフラグ */);
                        bufferedOutputStream.write(0x03/* テキストのフレームの文字コード。UTF-8は16進数で03。 */);

                        byte[] imageMimetypeByteArray = imageMimetype.getBytes(StandardCharsets.UTF_8);

                        for (int index = 0; index < imageMimetypeByteArray.length; index++) {
                            bufferedOutputStream.write(imageMimetypeByteArray[index]);
                        }

                        bufferedOutputStream.write(0x00/* NULLの文字コード */);
                        bufferedOutputStream.write(0x03/* Picture Type(画像の種類)。Front Cover(表カバー)は16進数で03。 */);
                        bufferedOutputStream.write(0x00/* Description(説明)の終了を表すNULLの文字コード。 */);

                        byte[] imageByteArray = new byte[imageByteList.size()];
                        for (int index = 0; index < imageByteArray.length; index++) {
                            imageByteArray[index] = imageByteList.get(index);
                        }

                        for (int index = 0; index < imageByteArray.length; index++) {
                            bufferedOutputStream.write(imageByteArray[index]);
                        }
                    }

                    byte[] mpegFrameByteArray = new byte[mpegFrameByteList.size()];
                    for (int index = 0; index < mpegFrameByteArray.length; index++) {
                        mpegFrameByteArray[index] = mpegFrameByteList.get(index);
                    }

                    for (int index = 0; index < mpegFrameByteArray.length; index++) {
                        bufferedOutputStream.write(mpegFrameByteArray[index]);
                    }
                }

                JOptionPane.showMessageDialog(frame, "新MP3ファイルの作成が完了しました。");

            } catch (Exception exception) {
                JOptionPane.showMessageDialog(frame, "エラー: " + exception);
                throw new RuntimeException(exception);
            }
        });


        frame.setVisible(true); //ウィンドウを表示
    }
}
