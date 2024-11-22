using System.Collections;
using System.Collections.Generic;
using UnityEngine;

[System.Serializable]
public class AllData
{
    public Cars cars;
    public Stoplights stoplights;

    public static AllData CreateFromJSON(string jsonString)
    {
        return JsonUtility.FromJson<AllData>(jsonString);
    }
}