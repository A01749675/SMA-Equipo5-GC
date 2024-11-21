using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Networking;
public class Connection : MonoBehaviour
{

    List<List<Vector3>> positions;
    List<Stoplight> stoplights;
    List<Car> carData;
    AllData allData;
    Movement2 move;
    float time;
    float timeToUpdate;

    public bool addingPos;
    int llamadas;

    public List<StopLightControl> stopLightControls;


    IEnumerator RequestCarPositions()
    {
        addingPos = true;
        move.waitingForNextPos = true;
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/carData";
        using (UnityWebRequest www = UnityWebRequest.Post(url,form))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type","application/json");
            yield return www.SendWebRequest();
            if(www.result == UnityWebRequest.Result.ConnectionError){
                Debug.Log(www.error);
            }
            else{
                string response = www.downloadHandler.text;
                carData = Cars.CreateFromJSON(response).cars;

                foreach(Car car in carData)
                {
                    //Debug.Log("Got the position to start-------------------------------------------");
                    //Debug.Log(car.x+ " "+car.z);
                    move.setX(car.x);
                    move.setZ(car.z);
                    //move.setAngle(car.direction);

                }
                addingPos = false;
                move.waitingForNextPos = false;
                
            }
        }
        llamadas +=1;
        //Debug.Log(llamadas);
    }

 IEnumerator RequestAllData()
    {
        addingPos = true;
        move.waitingForNextPos = true;
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/carData";
        using (UnityWebRequest www = UnityWebRequest.Post(url,form))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type","application/json");
            yield return www.SendWebRequest();
            if(www.result == UnityWebRequest.Result.ConnectionError){
                Debug.Log(www.error);
            }
            else{
                string response = www.downloadHandler.text;
                allData = AllData.CreateFromJSON(response);
                Cars cars = allData.cars;
                Stoplights stoplights = allData.stoplights;
                foreach(Car car in cars.cars)
                {
                    Debug.Log("Got the position to start-------------------------------------------");
                    //Debug.Log(car.x+ " "+car.z);
                    move.setX(car.x-0.5f);
                    move.setZ(car.z-0.5f);

                }
            }
        }
    }

    IEnumerator RequestStoplightData()
    {
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/stoplightData";
        using (UnityWebRequest www = UnityWebRequest.Post(url,form))
        {
            www.downloadHandler = new DownloadHandlerBuffer();
            www.SetRequestHeader("Content-Type","application/json");
            yield return www.SendWebRequest();
            if(www.result == UnityWebRequest.Result.ConnectionError){
                Debug.Log(www.error);
            }
            else{
                string response = www.downloadHandler.text;
                stoplights = Stoplights.CreateFromJSON(response).stoplights;
                foreach(Stoplight stoplight in stoplights){
                    Debug.Log(stoplight.id+ " "+stoplight.state);
                    foreach(StopLightControl stopLightControl in stopLightControls){
                        stopLightControl.setState(stoplight.id,stoplight.state);
                    }
                }
            }
        }
    }



    // Start is called before the first frame update
    void Start()
    {
        llamadas=0;
        timeToUpdate = 1.0f;
        move = GetComponent<Movement2>();
        //StartCoroutine(RequestCarPositions());
        //StartCoroutine(RequestStoplightData());
    }

    // Update is called once per frame
    void Update()
    {
        if(move.callForNextPos && !addingPos){
            StartCoroutine(RequestCarPositions());
            StartCoroutine(RequestStoplightData());
            move.callForNextPos = false;
        }
    }

    public void CallNextPos(){
        StartCoroutine(RequestCarPositions());
        StartCoroutine(RequestStoplightData());
    }
}
