import com.nerox.client.modules.XSAce;

import java.net.InetSocketAddress;

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
            jac.doAction().eth.transfer("", "", "", 0 ,0 ,0);
            jac.doAction().dai.getBalance("asdasd");
            jac.doAction().thr.createAccount("");
            jac.doAction().btc.getRawPrivateKey();
            jac.doAction().btc.getPrivateKey();
            jac.doAction().btc.getAddress();
            jac.doAction().btc.getTransactionStatus("");

        }catch (IllegalArgumentException portException){
            throw new RuntimeException("Invalid port number the port number must be a number between 0 and" +
                    " 65535...");
        }catch (SecurityException securityManager){
            throw new SecurityException("There is a security manager in the system please verify that this software," +
                    "has the permission to use internet");
        }
    }
}