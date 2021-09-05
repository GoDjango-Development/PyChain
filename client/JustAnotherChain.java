import com.nerox.client.callbacks.IUDPKeepCallback;
import com.nerox.client.keepalives.UDPKeepAlive;
import com.nerox.client.modules.XSAce;

public final class JustAnotherChain{
    private final JustAnotherAction action;
    private final XSAce ace;
    private static final String pathToServerSide = "/opt/PychainFramework/__main__.py";
    public JustAnotherChain(String address, int port, String publicKey, String hash, int length,
                            String versionProtocol, String serverKey) {
        JustAnotherCallback callback = new JustAnotherCallback();
        this.ace = new XSAce(
                address,
                port,
                publicKey,
                hash,
                length,
                versionProtocol,
                callback
        );
        this.ace.connect(UDPKeepAlive.TYPE.UDP_PROCHECK, 2, 2, 2);
        /*ITfprotocolCallback tfCallback = new ITfprotocolCallback() {
            @Override
            public void responseServerCallback(StatusInfo statusInfo) {
                throw new RuntimeException("Shouldnt be here");
            }

            @Override
            public void instanceTfProtocol(Tfprotocol tfprotocol) {
                throw new RuntimeException("Shouldnt be here");
            }

            @Override
            public void echoCallback(String value) {
                System.out.println(value);
            }
        };
        try {
            new Tfprotocol(ace,tfCallback).echoCommand("Hola mundo");
        }catch (IOException exception){
            throw new RuntimeException(exception);
        }
        action = null;
        if (true) return; // True
        */
        UDPKeepAlive.SetCallback(new IUDPKeepCallback() {
            @Override
            public void ConnectionClosed() {
                callback.releaseAllThreads();
            }
        });
        this.ace.startCommand();
        this.ace.inskeyCommand(serverKey);
        this.action = JustAnotherAction.instanceOf(this.ace, pathToServerSide);
    }

    public JustAnotherAction doAction(){
        return this.action;
    }
    public void endJAC(){
        try {
            this.finalize();
        } catch (Throwable e) {
            e.printStackTrace();
        }
    }
    @Override
    protected void finalize() throws Throwable {
        System.out.println("Finalizing...");
        ((JustAnotherCallback)this.ace.getProtoHandler()).putInOutPocket("quit");
        super.finalize();
    }

    public static void main(String [] args){
        try{
            JustAnotherChain jac = new JustAnotherChain(
                    "tfproto.expresscuba.com",10347,
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
            //if (true) return; // testing purpose
            int choice = 1;
            switch (choice){
                case 0: {
                    System.out.println(jac.doAction().trx.setProvider("https://api.shasta.trongrid.io",
                            "a71bd239-49a2-44c4-a10c-d86c051e6f01"));
                    System.out.println(jac.doAction().trx
                            .setAccount("907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53"));
                    System.out.println(jac.doAction().trx.getBalance("TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof"));
                    System.out.println(jac.doAction().trx.getRawPrivateKey());
                    System.out.println(jac.doAction().trx.getPrivateKey());
                    System.out.println(jac.doAction().trx.getAddress());
                    System.out.println(jac.doAction().trx.getPublicKey("TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof"));

                    System.out.println(jac.doAction()
                            .trx.getTransactionStatus("5cb046e5d6a9340b4a534ba3ee837e1d597d935bd59b08e29ebfc8ea418832ac"));
                    System.out.println(jac.doAction().trx.transfer("TFysCB929XGezbnyumoFScyevjDggu3BPq",
                            "907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53",
                            "TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof", 5 ,10));
                    System.out.println(jac.doAction().trx.createAccount("",""));
                    break;
                }
                case 1: {
                    System.out.println(jac.doAction().eth
                            .setProvider("https://ropsten.infura.io/v3/0893ea819efe41509c62b3c0faefc5ea"));
                    //System.out.println(jac.doAction().eth.createAccount(""));

                    System.out.println(jac.doAction().eth
                            .setAccount("78ebaebce1fb9f3ca35112557ec202abf43cea029c752f25230a43a266c1877f"));

                    System.out.println(jac.doAction().eth.getBalance());

                    System.out.println(jac.doAction().eth.getRawPrivateKey());

                    System.out.println(jac.doAction().eth.getPrivateKey());

                    System.out.println(jac.doAction().eth.getAddress());

                    System.out.println(jac.doAction().eth.getPublicKey(
                            "0x4f571faC1ecb15C9C5b125653F56A83B6B4aC917"));

                    System.out.println(jac.doAction()
                            .eth.getTransactionStatus(
                                    "0x60c27b4402d313f0a0a15911a074c899d5a5639293504f9ecdc98ecaf1e32077"));
                    // System.out.println(jac.doAction().eth.transfer("TFysCB929XGezbnyumoFScyevjDggu3BPq",
                    //         "907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53",
                    //         "TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof", 5 ,10, 10));

                    break;
                }
                case 2: {

                    System.out.println(jac.doAction().dai
                            .setProvider("https://rinkeby.infura.io/v3/0893ea819efe41509c62b3c0faefc5ea"));
                    //System.out.println(jac.doAction().eth.createAccount(""));

                    System.out.println(jac.doAction().dai
                            .setAccount("7fcb64f5067de3d97998bee741e856e35edf9f819d4ee14c48f7beb49b7647b0"));

                    System.out.println(jac.doAction().dai.getBalance());

                    System.out.println(jac.doAction().dai.getRawPrivateKey());

                    System.out.println(jac.doAction().dai.getPrivateKey());

                    System.out.println(jac.doAction().dai.getAddress());

                    System.out.println(jac.doAction().dai.getPublicKey(
                            "0x4f571faC1ecb15C9C5b125653F56A83B6B4aC917"));

                    System.out.println(jac.doAction()
                            .dai.getTransactionStatus(
                                    "0x60c27b4402d313f0a0a15911a074c899d5a5639293504f9ecdc98ecaf1e32077"));
                    // System.out.println(jac.doAction().eth.transfer("TFysCB929XGezbnyumoFScyevjDggu3BPq",
                    //         "907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53",
                    //         "TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof", 5 ,10, 10));
                    //jac.finalize();
                    //System.out.println("END OF ALL");
                    break;
                }
                case 3: {
                    //System.out.println(jac.doAction().btc
                    //        .setProvider("http://myrpc01:password01@localhost:18332"));
                    System.out.println(jac.doAction().btc
                            .setProvider("myrpc01", "password01", "tfproto.expresscuba.com",
                                    18332, "https"));
                    System.out.println(jac.doAction().btc.createWallet("newOne", "holahola"));
                    System.out.println(jac.doAction().btc.unlockWallet("holahola",10000));
                    //System.out.println(jac.doAction().btc
                    //        .setAccount("7fcb64f5067de3d97998bee741e856e35edf9f819d4ee14c48f7beb49b7647b0"));

                    System.out.println(jac.doAction().btc.getBalance());

                    System.out.println(jac.doAction().btc.getRawPrivateKey());

                    System.out.println(jac.doAction().btc.getPrivateKey());

                    System.out.println(jac.doAction().btc.getAddress());

                    //System.out.println(jac.doAction().btc.getPublicKey(
                    //        "0x4f571faC1ecb15C9C5b125653F56A83B6B4aC917"));

                    //System.out.println(jac.doAction()
                    //        .btc.getTransactionStatus(
                    //                "0x60c27b4402d313f0a0a15911a074c899d5a5639293504f9ecdc98ecaf1e32077"));
                    // System.out.println(jac.doAction().eth.transfer("TFysCB929XGezbnyumoFScyevjDggu3BPq",
                    //         "907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53",
                    //         "TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof", 5 ,10, 10));
                    //jac.finalize();
                    //System.out.println("END OF ALL");
                    break;
                }
                case 4: {
                    System.out.println(jac.doAction().thr.setProvider("https://api.trongrid.io",
                            "a71bd239-49a2-44c4-a10c-d86c051e6f01"));
                    System.out.println(jac.doAction().thr.setTokenType("usdt-trc20"));
                    System.out.println(jac.doAction().thr
                            .setAccount("907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53"));
                    System.out.println(jac.doAction().thr.getBalance("TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof"));
                    System.out.println(jac.doAction().thr.getRawPrivateKey());
                    System.out.println(jac.doAction().thr.getPrivateKey());
                    System.out.println(jac.doAction().thr.getAddress());
                    System.out.println(jac.doAction().thr.getPublicKey("TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof"));

                    System.out.println(jac.doAction()
                            .trx.getTransactionStatus("5cb046e5d6a9340b4a534ba3ee837e1d597d935bd59b08e29ebfc8ea418832ac"));
                    System.out.println(jac.doAction().thr.transfer("TFysCB929XGezbnyumoFScyevjDggu3BPq",
                            "907fd95e74362d5262124ac953ef86995db891697d91c6cf68a535ba8a915f53",
                            "TJTzrLRrHHPbdSMcwoS87QYLnXHmUACUof", 5 ,10));
                    System.out.println(jac.doAction().thr.createAccount("",""));
                    break;
                }
                default:{
                    throw new Exception("Should not be here");
                }
            }
            jac.endJAC();
        } catch (SecurityException securityManager){
            throw new SecurityException("There is a security manager in the system please verify that this software," +
                    "has the permission to use internet");
        } catch (Throwable throwable) {
            throw new RuntimeException(throwable);
        }
    }
}