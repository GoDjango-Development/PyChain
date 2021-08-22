import com.nerox.client.callbacks.IXSAceCallback;
import com.nerox.client.constants.XSACEConsts;
import com.nerox.client.misc.StatusInfo;
import com.nerox.client.modules.XSAce;

import java.util.ArrayList;

public final class JustAnotherCallback implements IXSAceCallback {
    private Object lastResult;
    private boolean isRunning = true;
    private final Object mutex = new Object();
    private final ArrayList<String> outPocket = new ArrayList<>();
    private final ArrayList<String> inPocket = new ArrayList<>();
    public synchronized void putInOutPocket(String coin){
        System.out.println(coin);
        this.outPocket.add(coin);
        synchronized (this.mutex){
            this.mutex.notifyAll();
        }
    }
    private synchronized void saveInPocket(String result){
        this.inPocket.add(result);
    }
    public ArrayList<String> checkPocket(){
        return (ArrayList<String>) this.inPocket.clone();
    }

    public Object getLastResult() {
        return lastResult;
    }

    @Override
    public void xsAceCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void inskeyCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void exitCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void goBackCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void setArgsCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void runNNLSizeCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void runBufSZCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void setRunBufCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void setRunLNCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void runWriteCallback(XSAce.Communication communication) {

    }

    @Override
    public void runReadCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }
    @Override
    public void runWriteNNLCallback(XSAce.Communication communication) {
        synchronized (this.mutex){
            while (isRunning){
                try {
                    this.mutex.wait();
                    for (int i = 0; i < this.outPocket.size(); i++){
                        String nextCommand = this.outPocket.remove(i);
                        communication.send(nextCommand.getBytes());
                        if (nextCommand.equals("quit")){
                            break;
                        }
                    }
                } catch (InterruptedException ignored) {}
            }
        }
    }

    @Override
    public void runReadNLCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
        this.saveInPocket(statusInfo.getMessage());
        if (statusInfo.getCode() == XSACEConsts.Commands.FINISHED) {
            this.isRunning = false;
            synchronized (this.mutex){
                this.mutex.notifyAll();
            }
        }
    }

    @Override
    public void runWriteBufCallback(XSAce.Communication communication) {

    }

    @Override
    public void runReadBufCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void statusServer(StatusInfo statusInfo) {
        System.out.println("*******************************");
        System.out.println(statusInfo.getStatus().name());
        System.out.println(statusInfo.getCode());
        System.out.println(statusInfo.getMessage());
        if (statusInfo.getPayload() != null)
            System.out.println(new String(statusInfo.getPayload()));
        System.out.println("*******************************");
        this.lastResult = statusInfo;
    }

    @Override
    public void responseServerCallback(StatusInfo statusInfo) {
        this.statusServer(statusInfo);
    }

    @Override
    public void instanceTfProtocol(XSAce xsAce) {

    }
}
