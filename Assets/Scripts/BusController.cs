using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BusController : MonoBehaviour
{
    [SerializeField]
    public GameObject busesPrefab;
    [SerializeField]
    public GameObject busesPrefab2;
    [SerializeField]
    public GameObject busesPrefab3;
    public bool callForNextPos;
    public bool waitingForNextPos;
    [SerializeField]
    Connection con;
    bool started;
    public int numberOfbuses;
    public List<float> startx;
    public List<float> startz;
    public List<string> startangle ;
    
    List<GameObject> buses; // Initialize the list

    List<bool> arrived;

    // Start is called before the first frame update
    void Start()
    {
        started = false;
        waitingForNextPos = false;
        callForNextPos = true;
        startx = new List<float>();
        startz = new List<float>();
        startangle = new List<string>();
        buses = new List<GameObject>();
        arrived = new List<bool>();
        //GameObject bus = Instantiate(busesPrefab);
        //bus.transform.position = new Vector3(13, 0, 8);
        
    }

    // Update is called once per frame
    void Update()
    {
        if(!started){
            //DebugLog("Not started");
            if(!callForNextPos && !con.addingPos){
                for (int i = 0; i < numberOfbuses; i++)
                    {
                    GameObject bus = new GameObject("EmptyObject");
                    bus.AddComponent<Movement>();
                    Movement2 movement = bus.GetComponent<Movement2>();
                    if (i % 3 == 0)
                    {
                        movement.busPrefab = busesPrefab;
                    }
                    else if (i % 2 == 0)
                    {
                        movement.busPrefab = busesPrefab2;
                    }
                    else if (i % 1 == 0)
                    {
                        movement.busPrefab = busesPrefab3;
                    }
                    movement.id = i;
                    bus.name = "bus" + i;
                    buses.Add(bus); 
                    movement.con = con;
                    movement.setAngle(startangle[i]);
                    movement.setX(startx[i]);
                    movement.setZ(startz[i]);
                    arrived.Add(false);
                    movement.busController = this;
                    //movement.getStarted = true;
                    movement.setInitialPos(startx[i],startz[i],startangle[i]);
                    movement.getStarted=true;
                }
                started = true;
            }
        }
        /*else{
            bool allbusessReady = true;
            foreach (GameObject bus in buses)
            {
                Movement movement = bus.GetComponent<Movement>();
                //Debug.Log("bus " + movement.id + " " + movement.callForNextPos);
                if (!movement.callForNextPos)
                {
                    allbusessReady = false;
                    break;
                }
            }

            if (allbusessReady && !waitingForNextPos)
            {
                //Debug.Log("Calling for next pos");
                foreach (GameObject bus in buses)
                {
                    Movement movement = bus.GetComponent<Movement>();
                    movement.waitingForNextPos = true;
                }
                callForNextPos = true;
            } else{
                Debug.Log("Not all buses ready");
            }
            /*else {
                foreach (GameObject bus in buses)
            {
                Movement movement = bus.GetComponent<Movement>();
                movement.callForNextPos = false;
                movement.waitingForNextPos = false;
                movement.getStarted = true;
            } 

            }
        }*/
    }

    public void setX(float x, int id)
    {
        if(started){
            if(!arrived[id]){
                GameObject bus = buses[id];
                Movement movement = bus.GetComponent<Movement>();
                movement.setX(x);
            }
        } else {
            startx.Add(x);
        }
    }
    public void setZ(float z, int id)
    {
        if(started){
            if(!arrived[id]){
                GameObject bus = buses[id];
                Movement2 movement = bus.GetComponent<Movement2>();
                movement.setZ(z);
            }
        } else{
            startz.Add(z);
        }
    }
    public void setAngle(string direction, int id)
    {
        if(started){
            if(!arrived[id]){
                GameObject bus = buses[id];
                Movement2 movement = bus.GetComponent<Movement2>();
                movement.setAngle(direction);
                movement.callForNextPos = false;
                movement.waitingForNextPos = false;
                movement.getStarted = true;
            }
        }
        else{
            startangle.Add(direction);
        }
    }
    public void setNoC(int noC)
    {
        numberOfbuses = noC;
    }
    public void setArrived(int id)
    {
        if(started){
            Debug.Log("bus "+id+" has arrived");
            GameObject bus = buses[id];
            Movement2 movement = bus.GetComponent<Movement2>();
            movement.setArrived();
            arrived[id] = true;
        }
    }

    public void trycalling(){
        bool allbusessReady = true;
            foreach (GameObject bus in buses)
            {
                Movement2 movement = bus.GetComponent<Movement2>();
                //Debug.Log("bus " + movement.id + " " + movement.callForNextPos);
                if (!movement.callForNextPos)
                {
                    allbusessReady = false;
                    break;
                }
            }

            if (allbusessReady && !waitingForNextPos)
            {
                //Debug.Log("Calling for next pos");
                foreach (GameObject bus in buses)
                {
                    Movement2 movement = bus.GetComponent<Movement2>();
                    movement.waitingForNextPos = true;
                }
                callForNextPos = true;
            } else{
                Debug.Log("Not all buses ready");
            }
    }
}