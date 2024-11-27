using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PedController : MonoBehaviour
{
    [SerializeField]
    GameObject pedPrefab;
    [SerializeField]
    GameObject pedPrefab2;
    [SerializeField]
    GameObject pedPrefab3;
    [SerializeField]
    GameObject pedPrefab4;
    public bool callForNextPos;
    public bool waitingForNextPos;
    [SerializeField]
    Connection con;
    bool started;
    public int numberOfpeds;
    public List<float> startx;
    public List<float> startz;
    public List<string> startangle ;
    
    List<GameObject> peds; // Initialize the list

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
        peds = new List<GameObject>();
        arrived = new List<bool>();
        
    }

    // Update is called once per frame
    void Update()
    {
        if(!started){
            //DebugLog("Not started");
            if(!callForNextPos && !con.addingPos){
                Debug.Log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
                for (int i = 0; i < numberOfpeds; i++)
                    {
                    GameObject ped = new GameObject("EmptyObject");
                    ped.AddComponent<Movement3>();
                    Movement3 movement = ped.GetComponent<Movement3>();
                    if (i % 4 == 0)
                    {
                        movement.pedPrefab = pedPrefab;
                    }
                    else if (i % 3 == 0)
                    {
                        movement.pedPrefab = pedPrefab2;
                    }
                    else if (i % 2 == 0)
                    {
                        movement.pedPrefab = pedPrefab3;
                    }
                    else
                    {
                        movement.pedPrefab = pedPrefab4;
                    }
                    movement.id = i;
                    ped.name = "ped" + i;
                    peds.Add(ped); 
                    movement.con = con;
                    //movement.setAngle(startangle[i]);
                    movement.setX(startx[i]);
                    movement.setZ(startz[i]);
                    arrived.Add(false);
                    movement.setInitialPos(startx[i],startz[i],"E");
                    movement.pedController = this;
                    Debug.Log("ped "+i+" added");
                    Debug.Log("get started");
                    movement.getStarted=true; 
                }
                started = true;
            }
        }
        /*else{
            bool allpedsReady = true;
            foreach (GameObject ped in peds)
            {
                Movement movement = ped.GetComponent<Movement>();
                //Debug.Log("ped " + movement.id + " " + movement.callForNextPos);
                if (!movement.callForNextPos)
                {
                    allpedsReady = false;
                    break;
                }
            }

            if (allpedsReady && !waitingForNextPos)
            {
                //Debug.Log("Calling for next pos");
                foreach (GameObject ped in peds)
                {
                    Movement movement = ped.GetComponent<Movement>();
                    movement.waitingForNextPos = true;
                }
                callForNextPos = true;
            } else{
                Debug.Log("Not all peds ready");
            }
            /*else {
                foreach (GameObject ped in peds)
            {
                Movement movement = ped.GetComponent<Movement>();
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
            
            GameObject ped = peds[id-1];
            Movement3 movement = ped.GetComponent<Movement3>();
            movement.setX(x);
            
            
        } else {
            startx.Add(x);
        }
    }
    public void setZ(float z, int id)
    {
        if(started){
           
                GameObject ped = peds[id-1];
                Movement3 movement = ped.GetComponent<Movement3>();
                movement.setZ(z);
                movement.callForNextPos = false;
                movement.waitingForNextPos = false;

        } else{
            startz.Add(z);
        }
    }
    public void setAngle(string direction, int id)
    {
        if(started){
            if(!arrived[0]){
                GameObject ped = peds[id-1];
                Movement3 movement = ped.GetComponent<Movement3>();
                movement.setAngle(direction);
                movement.callForNextPos = false;
                movement.waitingForNextPos = false;
                //movement.getStarted = true;
            }
        }
        else{
            startangle.Add(direction);
        }
    }
    public void setNoC(int noC)
    {
        numberOfpeds = noC;
    }
    public void setArrived(int id)
    {
        if(started){
            //Debug.Log("ped "+id+" has arrived");
            GameObject ped = peds[id-1];
            Movement3 movement = ped.GetComponent<Movement3>();
            movement.setArrived();
            arrived[0] = true;
        }
    }

    public void trycalling(){
        bool allpedsReady = true;
            foreach (GameObject ped in peds)
            {
                Movement3 movement = ped.GetComponent<Movement3>();
                //Debug.Log("ped " + movement.id + " " + movement.callForNextPos);
                if (!movement.callForNextPos)
                {
                    allpedsReady = false;
                    break;
                }
            }

            if (allpedsReady && !waitingForNextPos)
            {
                //Debug.Log("Calling for next pos");
                foreach (GameObject ped in peds)
                {
                    Movement3 movement = ped.GetComponent<Movement3>();
                    movement.waitingForNextPos = true;
                }
                callForNextPos = true;
            } else{
                //Debug.Log("Not all peds ready");
            }
    }

    public void setCrossing(bool crossing, int id)
    {
        if(started){
            GameObject ped = peds[id-1];
            Movement3 movement = ped.GetComponent<Movement3>();
            movement.setCrossing(crossing);
        }

    }

    public void setInBus(bool inBus, int id)
    {
        if(started){
            GameObject ped = peds[id-1];
            Movement3 movement = ped.GetComponent<Movement3>();
            movement.setInBus(inBus);
        }
    }
}