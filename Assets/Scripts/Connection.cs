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
    [SerializeField]
    CarController carController;
    

    public bool addingPos;
    int llamadas;

    public List<StopLightControl> stopLightControls;


    IEnumerator RequestCarPositions()
    {
        addingPos = true;
        carController.waitingForNextPos = true;
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
                    carController.setX(car.x,car.id);
                    carController.setZ(car.z,car.id);
                    carController.setAngle(car.direction,car.id);
                    if(car.arrived){
                        carController.setArrived(car.id);
                    }

                }
                addingPos = false;
                carController.waitingForNextPos = false;

                
            }
        }
        //llamadas +=1;
        //Debug.Log(llamadas);
    }

 IEnumerator RequestAllData()
    {
        llamadas +=1;
        addingPos = true;
        carController.waitingForNextPos = true;
        Debug.Log("Requesting all data");
        //addingPos = true;
        //move.waitingForNextPos = true;
        WWWForm form = new WWWForm();
        string url = "http://localhost:8000/allData";
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
                //Debug.Log(response);
                allData = AllData.CreateFromJSON(response);
                //Debug.Log(allData.cars.Count);
                List<Car> cars = allData.cars;
                List<Stoplight> stoplights = allData.stoplights;
                carController.setNoC(allData.cars.Count);
                foreach(Car car in cars)
                {
                    //Debug.Log("Got the position to start-------------------------------------------");
                    //Debug.Log(car.x+ " "+car.z);
                    carController.setX(car.x,car.id);
                    carController.setZ(car.z,car.id);
                    carController.setAngle(car.direction,car.id);
                    if(car.arrived){
                        carController.setArrived(car.id);
                    }

                }
                foreach(Stoplight stoplight in stoplights){
                    //Debug.Log(stoplight.id+ " "+stoplight.state);
                    foreach(StopLightControl stopLightControl in stopLightControls){
                        stopLightControl.setState(stoplight.id,stoplight.state);
                    }
                }
                addingPos = false;
                carController.waitingForNextPos = false;
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
        //move = GetComponent<Movement>();
        //StartCoroutine(RequestCarPositions());
        //StartCoroutine(RequestStoplightData());
    }

    // Update is called once per frame
    void Update()
    {
        if(carController.callForNextPos && !addingPos){
            StartCoroutine(RequestAllData());   
            carController.callForNextPos = false;
            //Debug.Log(llamadas);
        }
    }

    public void CallNextPos(){
        StartCoroutine(RequestCarPositions());
        StartCoroutine(RequestStoplightData());
    }
    
    public void CallAllData(){
        //Debug.Log("Calling all data");
        StartCoroutine(RequestAllData());
    }
}
