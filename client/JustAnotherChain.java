import com.nerox.client.Tfprotocol;
import com.nerox.client.callbacks.ITfprotocolCallback;
import com.nerox.client.connection.Easyreum;
import com.nerox.client.misc.Filestat;
import com.nerox.client.misc.StatusInfo;
import com.nerox.client.modules.XSAce;

import java.io.IOException;
import java.io.RandomAccessFile;
import java.net.InetSocketAddress;
import java.util.Date;

public final class JustAnotherChain{
    private final JustAnotherAction action;
    private final XSAce ace;
    private static final String pathToServerSide = "/";
    public JustAnotherChain(InetSocketAddress address, String publicKey, String hash, int length,
                            String versionProtocol, String serverKey) {
        JustAnotherCallback callback = new JustAnotherCallback();
        this.ace = new XSAce(
                address.getAddress().getHostAddress(),
                address.getPort(),
                publicKey,
                hash,
                length,
                versionProtocol,
                callback
        );
        this.ace.connect();
        this.ace.startCommand();
        this.ace.inskeyCommand(serverKey);
        this.action = JustAnotherAction.instanceOf(this.ace, pathToServerSide);
    }

    public JustAnotherAction doAction(){
        return this.action;
    }

    @Override
    protected void finalize() throws Throwable {
        ((JustAnotherCallback)this.ace.getProtoHandler()).putInOutPocket("quit");
        super.finalize();
    }

    public static void main(String [] args){
        try{
            test callback = new test();
            Tfprotocol tfprotocol = new Tfprotocol(
                    "tfproto.expresscuba.com",
                    10345,
                    "-----BEGIN PUBLIC KEY-----\n"
                    + "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq2K/X7ZSKlrMBIrSY9G/\n"
                    + "LLB+0injPCX17U7vb8XedQbjBT2AJ+qxmT4VLR1EWnvdUdvxaX9kRahI4hlSnfWl\n"
                    + "IddPfJRPH97Rk0OlMEQBclhD4WL88T8o4lVu0nuo8UAjqY0As6g6ZCG1s/Wfr64N\n"
                    + "aSvFr8NAYIaTQ6PbKxiypTythsSAkp5eAMkaje/ZAhkY1h0zMz09eg17veED8dIb\n"
                    + "R5sc7j05ndDOGucqY4+u9F/CZQNyOysKcFYjtYz/pStBPYY8CcU82SwW0Y2tbzy2\n"
                    + "j30ADzroySlQw+VjcffrGJao9qea1GWGwGMv4d4baMxrZeid2uB7NMUdljW8owWa\n" + "VwIDAQAB\n"
                    + "-----END PUBLIC KEY-----\n",
                    "testhash",
                    36,
                    "0.0",
                    callback
            );
            tfprotocol.connect();
            try {
                RandomAccessFile fis;
                fis = new RandomAccessFile(
                        "/home/etherbeing/Works/proyectos/Osvaldo/Respuesta/PyChain/version/" +
                                "1.0.2/pychain", "r"
                );
                callback.total = fis.length();
                callback.jump = 10000000;
                tfprotocol.putCommand(fis, "pychain", 0, 10000000);
                fis.close();
            } catch (IOException ignored) {}
            if (true) return;
            JustAnotherChain jac = new JustAnotherChain(
                    new InetSocketAddress("tfproto.expresscuba.com", 10345),
                    "-----BEGIN PUBLIC KEY-----\n"
                        + "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAq2K/X7ZSKlrMBIrSY9G/\n"
                        + "LLB+0injPCX17U7vb8XedQbjBT2AJ+qxmT4VLR1EWnvdUdvxaX9kRahI4hlSnfWl\n"
                        + "IddPfJRPH97Rk0OlMEQBclhD4WL88T8o4lVu0nuo8UAjqY0As6g6ZCG1s/Wfr64N\n"
                        + "aSvFr8NAYIaTQ6PbKxiypTythsSAkp5eAMkaje/ZAhkY1h0zMz09eg17veED8dIb\n"
                        + "R5sc7j05ndDOGucqY4+u9F/CZQNyOysKcFYjtYz/pStBPYY8CcU82SwW0Y2tbzy2\n"
                        + "j30ADzroySlQw+VjcffrGJao9qea1GWGwGMv4d4baMxrZeid2uB7NMUdljW8owWa\n" + "VwIDAQAB\n"
                        + "-----END PUBLIC KEY-----\n",
                    "testhash",
                    36,
                    "0.0",
                    "esteban"
            );
            jac.doAction().trx.setProvider("https://api.trongrid.io", "asdasdasdsd");
        }catch (IllegalArgumentException portException){
            throw new RuntimeException("Invalid port number the port number must be a number between 0 and" +
                    " 65535...");
        }catch (SecurityException securityManager){
            throw new SecurityException("There is a security manager in the system please verify that this software," +
                    "has the permission to use internet");
        }
    }
}
class test implements ITfprotocolCallback{
    @Override
    public void echoCallback(String s) {

    }

    @Override
    public void mkdirCallback(StatusInfo statusInfo) {

    }

    @Override
    public void delCallback(StatusInfo statusInfo) {

    }

    @Override
    public void rmdirCallback(StatusInfo statusInfo) {

    }

    @Override
    public void copyCallback(StatusInfo statusInfo) {

    }

    @Override
    public void touchCallback(StatusInfo statusInfo) {

    }

    @Override
    public void dateCallback(Integer integer, StatusInfo statusInfo) {

    }

    @Override
    public void datefCallback(Date date, StatusInfo statusInfo) {

    }

    @Override
    public void dtofCallback(Date date, StatusInfo statusInfo) {

    }

    @Override
    public void ftodCallback(Integer integer, StatusInfo statusInfo) {

    }

    @Override
    public void fstatCallback(Filestat filestat, StatusInfo statusInfo) {

    }

    @Override
    public void fupdCallback(StatusInfo statusInfo) {

    }

    @Override
    public void cpdirCallback(StatusInfo statusInfo) {

    }

    @Override
    public void xcopyCallback(StatusInfo statusInfo) {

    }

    @Override
    public void xdelCallback(StatusInfo statusInfo) {

    }

    @Override
    public void xrmdirCallback(StatusInfo statusInfo) {

    }

    @Override
    public void xcpdirCallback(StatusInfo statusInfo) {

    }

    @Override
    public void lockCallback(StatusInfo statusInfo) {

    }

    @Override
    public void sendFileCallback(boolean b, String s, StatusInfo statusInfo, byte[] bytes) throws IOException {

    }

    @Override
    public void rcvFileCallback(boolean b, String s, StatusInfo statusInfo) throws IOException {

    }

    @Override
    public void lsCallback(StatusInfo statusInfo) throws IOException {

    }

    @Override
    public void lsrCallback(StatusInfo statusInfo) throws IOException {

    }

    @Override
    public void renamCallback(StatusInfo statusInfo) {

    }

    @Override
    public void keepAliveCallback(StatusInfo statusInfo) {

    }

    @Override
    public void loginCallback(StatusInfo statusInfo) {

    }

    @Override
    public void chmodCallback(StatusInfo statusInfo) {

    }

    @Override
    public void chownCallback(StatusInfo statusInfo) {

    }

    @Override
    public void getCanCallback(StatusInfo statusInfo, Easyreum easyreum) throws IOException {

    }

    @Override
    public void putCanCallback(StatusInfo statusInfo, Easyreum easyreum) {
    }

    @Override
    public void sha256Callback(StatusInfo statusInfo) {

    }

    @Override
    public void prockeyCallback(StatusInfo statusInfo) {

    }

    @Override
    public void freespCallback(StatusInfo statusInfo) {

    }

    @Override
    public void udateCallback(StatusInfo statusInfo) {

    }

    @Override
    public void ndateCallback(StatusInfo statusInfo) {

    }

    @Override
    public void getWriteCallback(Tfprotocol.Codes codes) {

    }

    @Override
    public void getReadCallback(StatusInfo statusInfo) {

    }
    public long total;
    public long count = 0;
    public long jump = 0;
    @Override
    public void putCallback(Tfprotocol.Codes codes) {
        if (count%100==0){
            System.out.println(count*100/total);
            System.out.println(count++);
            System.out.println(jump = count*jump);
        }
    }

    @Override
    public void putStatusCallback(StatusInfo statusInfo) {
        if (statusInfo != null){
            System.out.println("*******************************");
            System.out.println(statusInfo.getStatus().name());
            System.out.println(statusInfo.getCode());
            System.out.println(statusInfo.getMessage());
            if (statusInfo.getPayload() != null)
                System.out.println(new String(statusInfo.getPayload()));
            System.out.println("*******************************");
        }
    }

    @Override
    public void nigmaCallback(StatusInfo statusInfo) {

    }

    @Override
    public void statusServer(StatusInfo statusInfo) {

    }

    @Override
    public void responseServerCallback(StatusInfo statusInfo) {

    }

    @Override
    public void instanceTfProtocol(Tfprotocol tfprotocol) {

    }
}