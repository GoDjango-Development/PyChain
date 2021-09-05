import com.nerox.client.callbacks.IXSAceCallback;
import com.nerox.client.constants.XSACEConsts;
import com.nerox.client.misc.StatusInfo;
import com.nerox.client.modules.XSAce;

import java.util.ArrayList;

public final class JustAnotherCallback implements IXSAceCallback {
    static final String queryLimiter = "TF-RESULT: 400\n";
    private boolean isListening = false;
    private boolean isPendingNotifyToMutex = false;
    private Object lastResult;
    private boolean isRunning = true;
    private final Object mutex = new Object();
    private final ArrayList<String> outPocket = new ArrayList<>();
    private final ArrayList<String> incomingPocket = new ArrayList<>();
    private Object awaitingMutex;

    void clearIncomingPocket(){
        //System.out.println("When cleared data was : " + Arrays.toString(this.incomingPocket.toArray()));
        this.incomingPocket.clear();
    }
    void releaseAllThreads(){
        this.isRunning = false;
        this.isListening = false;
        synchronized (this.mutex){
            this.mutex.notifyAll();
        }
        synchronized (this.awaitingMutex){
            this.awaitingMutex.notifyAll();
        }
    }
    private void saveInPocket(String result){
        this.incomingPocket.add(result);
    }
    public void putInOutPocket(String coin){
        this.outPocket.add(coin);
        synchronized (this.mutex){
            this.mutex.notifyAll();
        }
    }
    public boolean isRunning(){
        return this.isRunning;
    }
    public void setWaitingMutex(final Object mutex){
        this.awaitingMutex = mutex;
    }
    Object getWaitingMutex(){
        return this.awaitingMutex;
    }
    public String retrieveFromPocket(){
        try {
            while (!this.incomingPocket.contains(queryLimiter) && this.isRunning){
                synchronized (this.awaitingMutex){
                    //System.out.println("Awaiting a response from JAAction");
                    this.awaitingMutex.wait();
                }
            }
        } catch (InterruptedException ignored) {}
        //System.out.println("Released from JAAction");
        if (this.isRunning && this.incomingPocket.size() > 0){
            String res = "";
            while (!this.incomingPocket.get(0).equals(queryLimiter)){
                res = res.concat(this.incomingPocket.get(0).replace(">> ",""));
                this.incomingPocket.remove(0);
            }
            this.incomingPocket.remove(0);
            return res;
        }
        return "";
    }


    public Object getLastResult() {
        return lastResult;
    }

    @Override
    public void startACECallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void inskeyCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void exitCallback(StatusInfo exit) {
        statusServer(exit);
    }
    @Override
    public void runWriteNNLCallback(XSAce.Communication communication) {
        while (isRunning){
            try {
                synchronized (this.mutex){
                    this.mutex.wait();
                }
                if (!isRunning) {
                    //System.out.println("Quitting write thread...");
                    break;
                }
                // communication.send_signal(XSACEConsts.Commands.SIGKILL);
                // if (true) continue;
                //System.out.println("Sending data to server, data is : "
                //        +  Arrays.toString(this.outPocket.toArray()));
                while(this.outPocket.size() > 0){
                    String nextCommand = this.outPocket.remove(0);
                    //System.out.println("Sending: "+ nextCommand);
                    communication.send(nextCommand.getBytes());
                    if (nextCommand.equals("quit")) {
                        //this.isRunning = false;
                        break;
                    }

                }
                //System.out.println("Data successfully send...");
            } catch (InterruptedException ignored) {}
        }
    }

    @Override
    public void runReadNLCallback(StatusInfo statusInfo) {
        //System.out.println("Replacing");
        //statusServer(statusInfo); // Only for testing purposes ("Comment this in production")
        //System.out.println(statusInfo.getStatus().name());
        //System.out.println(statusInfo.getCode());
        //System.out.println(statusInfo.getMessage());
        //System.out.println(statusInfo.getPayload().length);
        //if (true) return;
        if (statusInfo.getCode() == XSACEConsts.Commands.OK)
            synchronized (this.awaitingMutex){
                //System.out.println("Started and notify to constructor that should be waiting...");
                this.awaitingMutex.notifyAll();
                return;
            }
        else if (statusInfo.getCode() == XSACEConsts.Commands.FINISHED ||
                statusInfo.getCode() == XSACEConsts.Commands.ERROR
        ) {
            //this.communication.send_signal(XSACEConsts.Commands.OK);
            //System.out.println("Closing the client...");
            this.releaseAllThreads();
        }
        else if (this.isRunning){
            if (statusInfo.getMessage() == null || statusInfo.getMessage().isBlank())
                return;
            if (this.isListening)
                this.saveInPocket(statusInfo.getMessage());
            //else System.out.println(statusInfo.getMessage());
            if (statusInfo.getMessage().equals(queryLimiter)){
                if (!this.isListening){
                    this.isListening = true;
                }
                synchronized (this.awaitingMutex){
                    this.awaitingMutex.notifyAll();
                }
                System.gc();
                System.runFinalization();
            }
        }
        //System.out.println("Query limit reach it, awaking the mutexes");
    }

    @Override
    public void statusServer(StatusInfo statusInfo) {/*
        System.out.println("*******************************");
        System.out.println(statusInfo.getStatus().name());
        System.out.println(statusInfo.getCode());
        System.out.println(statusInfo.getMessage());
        if (statusInfo.getPayload() != null)
            System.out.println(new String(statusInfo.getPayload()));
        System.out.println("*******************************");*/
        this.lastResult = statusInfo;
    }

    @Override
    public void responseServerCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void instanceTfProtocol(XSAce xsAce) {}
}
