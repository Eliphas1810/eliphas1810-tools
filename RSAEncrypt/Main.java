import javax.swing.JFrame;
import java.awt.Container;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JTextField;
import javax.swing.JOptionPane;

import java.security.KeyFactory;
import java.security.PublicKey;
import java.security.spec.RSAPublicKeySpec;
import javax.crypto.Cipher;
import javax.crypto.CipherOutputStream;

import java.math.BigInteger;

import java.nio.file.Files;
import java.nio.file.Paths;

import java.io.InputStream;
import java.io.OutputStream;

public class Main {

    public static void main(String[] args) throws Exception {
        JFrame frame = new JFrame();
        frame.setTitle("RSA暗号化"); //ウィンドウのタイトルバーのタイトル
        frame.setSize(800, 300); //初期表示のウィンドウの横幅と高さ
        frame.setLocationRelativeTo(null); //モニターの中央に表示
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //ウィンドウ右上のXボタンで終了

        Container container = frame.getContentPane();
        container.setLayout(null); //LayoutManagerを使わず座標を指定して自由に配置

        JLabel inFileLabel = new JLabel("");
        inFileLabel.setSize(10, 10);
        inFileLabel.setLocation(10, 40); //座標を指定
        container.add(inFileLabel);

        JButton inFileSelectButton = new JButton("読み込みファイル選択");
        inFileSelectButton.setSize(240, 20);
        inFileSelectButton.setLocation(10, 10); //座標を指定
        container.add(inFileSelectButton);

        //読み込みファイル選択ボタンが押された時の処理
        inFileSelectButton.addActionListener(
            actionEvent -> {
                JFileChooser fileChooser = new JFileChooser();
                fileChooser.setFileSelectionMode(JFileChooser.FILES_ONLY);
                if (fileChooser.showOpenDialog(container) == JFileChooser.APPROVE_OPTION) {
                    inFileLabel.setText(fileChooser.getSelectedFile().getAbsolutePath());
                    inFileLabel.setSize(inFileLabel.getText().length() * 20, 10);
                }
            }
        );

        JLabel outDirLabel = new JLabel("");
        outDirLabel.setSize(10, 10);
        outDirLabel.setLocation(10, 90); //座標を指定
        container.add(outDirLabel);

        JButton outDirSelectButton = new JButton("書き込みディレクトリ選択");
        outDirSelectButton.setSize(240, 20);
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

        JLabel modulusLabel = new JLabel("Modulus(数学の法): ");
        modulusLabel.setSize(160, 10);
        modulusLabel.setLocation(10, 140); //座標を指定
        container.add(modulusLabel);

        JTextField modulusTextField = new JTextField(80);
        modulusTextField.setSize(200, 20);
        modulusTextField.setLocation(170, 140); //座標を指定
        container.add(modulusTextField);

        JLabel publicExponentLabel = new JLabel("Public Exponent(公開指数): ");
        publicExponentLabel.setSize(160, 10);
        publicExponentLabel.setLocation(10, 170); //座標を指定
        container.add(publicExponentLabel);

        JTextField publicExponentTextField = new JTextField(80);
        publicExponentTextField.setSize(200, 20);
        publicExponentTextField.setLocation(170, 170); //座標を指定
        container.add(publicExponentTextField);

        JButton encryptButton = new JButton("RSA暗号化");
        encryptButton.setSize(240, 20);
        encryptButton.setLocation(10, 200); //座標を指定
        container.add(encryptButton);

        //RSA暗号化ボタンが押された時の処理
        encryptButton.addActionListener(actionEvent -> {
            try {

                String inFile = inFileLabel.getText();
                String outDir = outDirLabel.getText();
                String modulusString = modulusTextField.getText();
                String publicExponentString = publicExponentTextField.getText();

                if (inFile.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "読み込みファイルを選択してください。");
                    return;
                }

                if (outDir.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "書き込みディレクトリを選択してください。");
                    return;
                }

                if (modulusString.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "Modulus(数学の法)を記入してください。");
                    return;
                }

                if (publicExponentString.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "Public Exponent(公開指数)を記入してください。");
                    return;
                }

                if (modulusString.matches("^[0-9]+$") == false) {
                    JOptionPane.showMessageDialog(frame, "半角数字でModulus(数学の法)を記入してください。");
                    return;
                }

                if (publicExponentString.matches("^[0-9]+$") == false) {
                    JOptionPane.showMessageDialog(frame, "半角数字でPublic Exponent(公開指数)を記入してください。");
                    return;
                }

                if (modulusString.matches("^0+$")) {
                    JOptionPane.showMessageDialog(frame, "1以上の数をModulus(数学の法)に記入してください。");
                    return;
                }

                if (publicExponentString.matches("^0+$")) {
                    JOptionPane.showMessageDialog(frame, "1以上の数をPublic Exponent(公開指数)に記入してください。");
                    return;
                }

                if (Files.exists(Paths.get(inFile)) == false) {
                    JOptionPane.showMessageDialog(frame, "読み込みファイルを選択し直してください。");
                    return;
                }

                if (Files.exists(Paths.get(outDir)) == false) {
                    JOptionPane.showMessageDialog(frame, "書き込みディレクトリを選択し直してください。");
                    return;
                }

                KeyFactory keyFactory = KeyFactory.getInstance("RSA");
                PublicKey publicKey = keyFactory.generatePublic(new RSAPublicKeySpec(new BigInteger(modulusString), new BigInteger(publicExponentString)));

                Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
                cipher.init(Cipher.ENCRYPT_MODE, publicKey);

                try (
                    InputStream inputStream = Files.newInputStream(Paths.get(inFile));
                    CipherOutputStream cipherOutputStream = new CipherOutputStream(
                        Files.newOutputStream(Paths.get(outDir).resolve(Paths.get(inFile).getFileName() + ".rsa.bin")),
                        cipher
                    );
                ) {
                    inputStream.transferTo(cipherOutputStream);
                }

                JOptionPane.showMessageDialog(frame, "RSA暗号化が完了しました。");

            } catch (Exception exception) {
                JOptionPane.showMessageDialog(frame, "エラー: " + exception);
                throw new RuntimeException(exception);
            }
        });

        frame.setVisible(true); //ウィンドウを表示
    }
}
