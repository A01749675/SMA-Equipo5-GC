using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class AllData
{
    public List<Car> cars;
    public List<Stoplight> stoplights;
    public List<Bus> buses;
    public List<Pedestrian> pedestrians;

    public static AllData CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<AllData>(jsonString);
    }
}