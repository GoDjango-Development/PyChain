import com.nerox.client.misc.StatusInfo;
import com.nerox.client.misc.StatusServer;
import com.nerox.client.modules.XSAce;

import java.util.MissingFormatArgumentException;

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
    private final JustAnotherCallback callback;
    public JustAnotherBase(JustAnotherCallback callback){
        this.callback = callback;
    }
    public boolean setProvider(String url, String apiKey, String user, String pass, String address, int port,
                               String protocol){
        StringBuilder builder = new StringBuilder();
        String env = this.getClass().getName().toLowerCase();
        builder.append(env);
        builder.append(" set-provider");
        if (env.equals(Bitcoin.class.getName().toLowerCase())){
            builder.append(" user ").append(user);
            builder.append(" pass ").append(pass);
            builder.append(" address ").append(address);
            builder.append(" port ").append(port);
            builder.append(" protocol ").append(protocol);
        }
        if (!apiKey.isEmpty())
            builder.append(" with ").append(apiKey);
        if (!url.isEmpty())
            builder.append(" url ").append(url);
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean getBalance(String of){
        StringBuilder builder = new StringBuilder();
        builder.append(this.getClass().getName().toLowerCase());
        builder.append(" get-balance ");
        if (!of.isEmpty())
            builder.append(" of ").append(of);
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean createAccount(String name){
        StringBuilder builder = new StringBuilder();
        String env = this.getClass().getName().toLowerCase();
        builder.append(env);
        builder.append(" create-account");
        if (env.equals(Bitcoin.class.getName().toLowerCase())){
            builder.append(" name ").append(name);
        }
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean createWallet(String name){
        return createAccount(name);
    }
    public boolean getPrivateKey(){
        StringBuilder builder = new StringBuilder();
        builder.append(this.getClass().getName().toLowerCase());
        builder.append(" get-prik ");
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean getRawPrivateKey(){
        StringBuilder builder = new StringBuilder();
        builder.append(this.getClass().getName().toLowerCase());
        builder.append(" get-raw-prik ");
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean getAddress(){
        StringBuilder builder = new StringBuilder();
        builder.append(this.getClass().getName().toLowerCase());
        builder.append(" get-address");
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean getPublicKey(String of){
        StringBuilder builder = new StringBuilder();
        String env = this.getClass().getName().toLowerCase();
        builder.append(env);
        builder.append(" get-pubk");
        if (env.equals(Bitcoin.class.getName().toLowerCase())){
            builder.append(" of ");
        }
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean getTransactionStatus(String of){
        StringBuilder builder = new StringBuilder();
        builder.append(this.getClass().getName().toLowerCase());
        builder.append(" get-tx-status");
        builder.append(" of ").append(of);
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }
    public boolean setAccount(){
        
    }
    protected boolean transfer(String to, String privateKey, float fee, boolean isReplaceable,
                            float gasPrice, float gasLimit, String from, float amount){
        StringBuilder builder = new StringBuilder();
        String env = this.getClass().getName().toLowerCase();
        builder.append(env);
        builder.append(" transfer");
        builder.append(" amount ").append(amount);
        if (env.equals("bitcoin")){
            builder.append(" replace ").append(isReplaceable);
            builder.append(" passphrase ").append(privateKey);
        }
        else if (!privateKey.isEmpty())
            builder.append(" with ").append(privateKey);
        else
            throw new MissingFormatArgumentException("Private Key or passphrase is required for a transaction" +
                    "always...");
        if (env.equals("ethereum")){
            builder.append(" gas-price ").append(gasPrice);
            builder.append(" gas-limit ").append(gasLimit);
        }else if (fee > 0){
                builder.append(" fee ").append(fee);
        }
        if (!from.isEmpty())
            builder.append(" from ").append(from);
        if (!to.isEmpty())
            builder.append(" to ").append(to);
        this.callback.putInOutPocket(builder.toString());
        return this.callback.checkPocket().contains("TF-RESULT: 400");
    }

}

final class Ethereum extends JustAnotherBase{
    public Ethereum(JustAnotherCallback callback) {
        super(callback);
    }
    public boolean transfer(String to, String privateKey, String from, float amount, float gasPrice,
                            float gasLimit){
        return super.transfer(to, privateKey, 0, false, gasPrice, gasLimit, from, amount);
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

    public boolean setProvider(String url, String apiKey) {
        return super.setProvider(url, apiKey, null, null, null, 0, null);
    }
}
