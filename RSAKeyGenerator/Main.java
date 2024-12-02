import javax.swing.JFrame;
import java.awt.Container;
import javax.swing.JLabel;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JTextField;
import javax.swing.JOptionPane;

import java.security.KeyPairGenerator;
import java.security.KeyPair;
import java.security.KeyFactory;
import java.security.spec.RSAPublicKeySpec;
import java.security.interfaces.RSAPublicKey;

import java.security.spec.RSAPrivateKeySpec;
import java.security.interfaces.RSAPrivateKey;

import java.nio.charset.Charset;

import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardOpenOption;

public class Main {

    public static void main(String[] args) throws Exception {
        JFrame frame = new JFrame();
        frame.setTitle("RSA暗号鍵生成"); //ウィンドウのタイトルバーのタイトル
        frame.setSize(800, 300); //初期表示のウィンドウの横幅と高さ
        frame.setLocationRelativeTo(null); //モニターの中央に表示
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE); //ウィンドウ右上のXボタンで終了

        Container container = frame.getContentPane();
        container.setLayout(null); //LayoutManagerを使わず座標を指定して自由に配置

        JLabel outDirLabel = new JLabel("");
        outDirLabel.setSize(10, 10);
        outDirLabel.setLocation(10, 40); //座標を指定
        container.add(outDirLabel);

        JButton outDirSelectButton = new JButton("書き込みディレクトリ選択");
        outDirSelectButton.setSize(240, 20);
        outDirSelectButton.setLocation(10, 10); //座標を指定
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
        modulusLabel.setSize(170, 10);
        modulusLabel.setLocation(10, 70); //座標を指定
        container.add(modulusLabel);

        JTextField modulusTextField = new JTextField(80);
        modulusTextField.setSize(200, 20);
        modulusTextField.setLocation(180, 70); //座標を指定
        container.add(modulusTextField);

        JLabel publicExponentLabel = new JLabel("Public Exponent(公開指数): ");
        publicExponentLabel.setSize(170, 10);
        publicExponentLabel.setLocation(10, 100); //座標を指定
        container.add(publicExponentLabel);

        JTextField publicExponentTextField = new JTextField(80);
        publicExponentTextField.setSize(200, 20);
        publicExponentTextField.setLocation(180, 100); //座標を指定
        container.add(publicExponentTextField);

        JLabel privateExponentLabel = new JLabel("Private Exponent(秘密指数): ");
        privateExponentLabel.setSize(170, 10);
        privateExponentLabel.setLocation(10, 130); //座標を指定
        container.add(privateExponentLabel);

        JTextField privateExponentTextField = new JTextField(80);
        privateExponentTextField.setSize(200, 20);
        privateExponentTextField.setLocation(180, 130); //座標を指定
        container.add(privateExponentTextField);

        JButton generateRsaKeyButton = new JButton("RSA暗号鍵生成");
        generateRsaKeyButton.setSize(240, 20);
        generateRsaKeyButton.setLocation(10, 160); //座標を指定
        container.add(generateRsaKeyButton);

        //RSA暗号化ボタンが押された時の処理
        generateRsaKeyButton.addActionListener(actionEvent -> {
            try {
                String outDir = outDirLabel.getText();

                if (outDir.isEmpty()) {
                    JOptionPane.showMessageDialog(frame, "書き込みディレクトリを選択してください。");
                    return;
                }

                if (Files.exists(Paths.get(outDir)) == false) {
                    JOptionPane.showMessageDialog(frame, "書き込みディレクトリを選択し直してください。");
                    return;
                }

                KeyPairGenerator keyPairGenerator = KeyPairGenerator.getInstance("RSA");
                keyPairGenerator.initialize(2048);
                KeyPair keyPair = keyPairGenerator.generateKeyPair();
                KeyFactory keyFactory = KeyFactory.getInstance("RSA");

                RSAPublicKeySpec publicKeySpec = keyFactory.getKeySpec(keyPair.getPublic(), RSAPublicKeySpec.class);
                RSAPublicKey rsaPublicKey = (RSAPublicKey)keyFactory.generatePublic(publicKeySpec);

                //rsaPublicKey.getEncoded(); //ASN.1形式の公開鍵の情報

                modulusTextField.setText(rsaPublicKey.getModulus().toString());

                Files.write(
                    Paths.get(outDir).resolve("modulus(数学の法).txt"),
                    rsaPublicKey.getModulus().toString().getBytes(Charset.forName("UTF-8")),
                    StandardOpenOption.CREATE
                );

                publicExponentTextField.setText(rsaPublicKey.getPublicExponent().toString());

                Files.write(
                    Paths.get(outDir).resolve("publicExponent(公開指数).txt"),
                    rsaPublicKey.getPublicExponent().toString().getBytes(Charset.forName("UTF-8")),
                    StandardOpenOption.CREATE
                );

                RSAPrivateKeySpec privateKeySpec = keyFactory.getKeySpec(keyPair.getPrivate(), RSAPrivateKeySpec.class);
                RSAPrivateKey rsaPrivateKey = (RSAPrivateKey)keyFactory.generatePrivate(privateKeySpec);

                //rsaPrivateKey.getEncoded(); //ASN.1形式の秘密鍵の情報

                privateExponentTextField.setText(rsaPrivateKey.getPrivateExponent().toString());

                Files.write(
                    Paths.get(outDir).resolve("privateExponent(秘密指数).txt"),
                    rsaPrivateKey.getPrivateExponent().toString().getBytes(Charset.forName("UTF-8")),
                    StandardOpenOption.CREATE
                );

                JOptionPane.showMessageDialog(frame, "RSA暗号鍵生成が完了しました。");

            } catch (Exception exception) {
                JOptionPane.showMessageDialog(frame, "エラー: " + exception);
                throw new RuntimeException(exception);
            }
        });

        frame.setVisible(true); //ウィンドウを表示
    }
}
