import com.nerox.client.misc.StatusInfo;
import com.nerox.client.misc.StatusServer;
import com.nerox.client.modules.XSAce;

public class JustAnotherAction {
    public final Ethereum eth;
    public final Bitcoin btc;
    public final Tether thr;
    public final Dai dai;
    public final Tron trx;

    private XSAce ace;
    private String pathToServer;
    public JustAnotherAction(XSAce ace, String pathToServer){
        this.ace = ace;
        JustAnotherCallback callback = (JustAnotherCallback) this.ace.getProtoHandler();
        eth = new Ethereum(callback);
        btc = new Bitcoin(callback);
        thr = new Tether(callback);
        trx = new Tron(callback);
        dai = new Dai(callback);

        this.pathToServer = pathToServer;
        if (!ace.isConnect())
            throw new RuntimeException("XSAce is not yet connected, at this point it should be, please check" +
                    " your internet connection before creating this instance...");
        new Thread(new Runnable() {
            @Override
            public void run() {
                ace.runNLCommand(pathToServer);
            }
        }).start();
        if (!((StatusInfo)callback.getLastResult()).getStatus().equals(StatusServer.OK)){
            throw new RuntimeException("Cannot successfully contact to backend please contact administrator");
        }
    }
    public static JustAnotherAction instanceOf(XSAce ace, String pathToServer){
        return new JustAnotherAction(ace, pathToServer);
    }
}
abstract class JustAnotherBase{
    JustAnotherCallback callback;
    public JustAnotherBase(JustAnotherCallback callback){
        this.callback = callback;
    }
    public boolean setProvider(String url, String apiKey){
        StringBuilder builder = new StringBuilder();
        builder.append(this.getClass().getName().toLowerCase());
        builder.append(" set-provider ");
        if (!apiKey.isEmpty())
            builder.append(" with ").append(apiKey);
        if (!url.isEmpty())
            builder.append(" url ").append(url);
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
}

final class Ethereum extends JustAnotherBase{
    public Ethereum(JustAnotherCallback callback) {
        super(callback);
    }
}
final class Bitcoin extends JustAnotherBase{
    public Bitcoin(JustAnotherCallback callback) {
        super(callback);
    }
}
final class Dai extends JustAnotherBase{
    public Dai(JustAnotherCallback callback) {
        super(callback);
    }
}
final class Tether extends JustAnotherBase{
    public Tether(JustAnotherCallback callback) {
        super(callback);
    }
}
final class Tron extends JustAnotherBase{
    public Tron(JustAnotherCallback callback) {
        super(callback);
    }
}
