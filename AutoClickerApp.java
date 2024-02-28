import javax.swing.*;
import java.awt.*;
import java.awt.event.InputEvent;
import java.util.concurrent.atomic.AtomicBoolean;
import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import org.jnativehook.mouse.NativeMouseEvent;
import org.jnativehook.mouse.NativeMouseAdapter;
import java.util.logging.Level;
import java.util.logging.Logger;

public class AutoClickerApp extends JFrame {
    private JLabel coordLabel1, coordLabel2, coordLabel3;
    private JRadioButton popupRadio, stayRadio;
    private JComboBox<Integer> popupTimeOption;
    private final AtomicBoolean running = new AtomicBoolean(false);
    private Point coord1 = new Point(0, 0);
    private Point coord2 = new Point(0, 0);
    private Point coord3 = new Point(0, 0);
    private int coordCount = 0;

    public AutoClickerApp() {
        setTitle("讲解点击-终极版");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLayout(new BoxLayout(getContentPane(), BoxLayout.Y_AXIS));
        setSize(690, 170);
        setResizable(false);
        initComponents();
        disableJNativeHookLogger();
    }

    private void initComponents() {
        // 创建包含坐标标签的面板
        JPanel labelPanel = new JPanel();
        labelPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
        coordLabel1 = new JLabel("[2链坐标] x: 0, y: 0");
        coordLabel2 = new JLabel("[1链坐标] x: 0, y: 0");
        coordLabel3 = new JLabel("[查询坐标] x: 0, y: 0");
        labelPanel.add(coordLabel1);
        labelPanel.add(coordLabel2);
        labelPanel.add(coordLabel3);
        add(labelPanel);

        // 创建包含按钮和其他控制元素的面板
        JPanel buttonPanel = new JPanel();
        buttonPanel.setLayout(new FlowLayout(FlowLayout.CENTER));
        JButton copyButton = new JButton("选择坐标");
        copyButton.addActionListener(e -> setupGlobalMouseListener());
        buttonPanel.add(copyButton);

        popupRadio = new JRadioButton("弹窗", true);
        stayRadio = new JRadioButton("常驻");
        ButtonGroup group = new ButtonGroup();
        group.add(popupRadio);
        group.add(stayRadio);
        buttonPanel.add(popupRadio);
        buttonPanel.add(stayRadio);

        Integer[] hours = {7, 11, 14};
        popupTimeOption = new JComboBox<>(hours);
        buttonPanel.add(popupTimeOption);

        JButton startButton = new JButton("开始");
        startButton.addActionListener(e -> startProgram());
        buttonPanel.add(startButton);

        JButton stopButton = new JButton("停止");
        stopButton.addActionListener(e -> stopProgram());
        buttonPanel.add(stopButton);

        // 将面板添加到窗体
        add(buttonPanel);
    }

    private void setupGlobalMouseListener() {
        try {
            GlobalScreen.registerNativeHook();
        } catch (NativeHookException ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());
            System.exit(1);
        }

        GlobalScreen.addNativeMouseListener(new NativeMouseAdapter() {
            @Override
            public void nativeMouseClicked(NativeMouseEvent e) {
                captureCoord(e.getX(), e.getY());
            }
        });
    }

    private void captureCoord(int x, int y) {
        switch (coordCount) {
            case 0:
                coord1.setLocation(x, y);
                coordLabel1.setText("[2链坐标] x: " + x + ", y: " + y);
                break;
            case 1:
                coord2.setLocation(x, y);
                coordLabel2.setText("[1链坐标] x: " + x + ", y: " + y);
                break;
            case 2:
                coord3.setLocation(x, y);
                coordLabel3.setText("[查询坐标] x: " + x + ", y: " + y);
                // Unregister native hook to stop listening to further mouse events
                try {
                    GlobalScreen.unregisterNativeHook();
                } catch (NativeHookException ex) {
                    ex.printStackTrace();
                }
                break;
        }
        coordCount++;
    }

    private void startProgram() {
        running.set(true);
        int duration = (Integer) popupTimeOption.getSelectedItem() * 3600; // Convert to seconds
        Thread clickThread = new Thread(() -> autoClick(duration));
        clickThread.start();
    }

    private void autoClick(int duration) {
        try {
            Robot robot = new Robot();
            long endTime = System.currentTimeMillis() + duration * 1000L;
            while (running.get() && System.currentTimeMillis() < endTime) {
                click(robot, coord1);
                click(robot, coord2);
                click(robot, coord3);
                Thread.sleep(popupRadio.isSelected() ? 9700 : 5000);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void click(Robot robot, Point coord) {
        robot.mouseMove(coord.x, coord.y);
        robot.mousePress(InputEvent.BUTTON1_DOWN_MASK);
        robot.mouseRelease(InputEvent.BUTTON1_DOWN_MASK);
    }

    private void stopProgram() {
        running.set(false);
    }

    private void disableJNativeHookLogger() {
        Logger logger = Logger.getLogger(GlobalScreen.class.getPackage().getName());
        logger.setLevel(Level.OFF); // Disable logging from JNativeHook
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            AutoClickerApp app = new AutoClickerApp();
            app.setVisible(true);
        });
    }
}
