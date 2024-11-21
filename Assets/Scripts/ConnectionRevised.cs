using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting;
using UnityEngine;
using UnityEngine.Networking;
public class ConnectionRevised : MonoBehaviour
{

    List<List<Vector3>> positions;
    List<Stoplight> stoplights;
    List<Car> carData;
    AllData allData;

    public bool addingPos;
    int llamadas;

    [SerializeField]
    Vehicles vehicles;  



 IEnumerator RequestAllData()
    {

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
                allData = AllData.CreateFromJSON(response);
                Cars cars = allData.cars;
                Stoplights stoplights = allData.stoplights;

                for(int i = 0; i < vehicles.numVehicles; i++){
                    vehicles.vehicles[i].AddPositions(new Vector3(cars.cars[i].x,0,cars.cars[i].z));
                }
            }
        }
    }



    // Start is called before the first frame update
    void Start()
    {
        bool start = false;
        while(!start){
            StartCoroutine(RequestAllData());
            foreach(Vehicle vehicle in vehicles.vehicles){
                start = vehicle.MetStartingConditions();
            }

        }
    }

    // Update is called once per frame
    void Update()
    {
        StartCoroutine(RequestAllData());
    }


}
