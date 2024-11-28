using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class CameraMovement : MonoBehaviour
{
    public float panespeed = 5.0f;

    public float rotatespeed = 2f;
    
    List<GameObject> allObjects = new List<GameObject>();
    // Start is called before the first frame update
    void Start()
    {
        allObjects.AddRange(FindObjectsOfType<GameObject>());
        allObjects.Remove(Camera.main.gameObject);
        Cursor.visible = false;
    }

    // Update is called once per frame
    void Update()
    {
        CheckObjectsInFrustum();
        if(Input.GetKey(KeyCode.D))
        {
            transform.Translate(new Vector3(panespeed * Time.deltaTime,0,0));
        }
        if(Input.GetKey(KeyCode.A))
        {
            transform.Translate(new Vector3(-panespeed * Time.deltaTime,0,0));
        }
        if(Input.GetKey(KeyCode.S))
        {
            transform.Translate(new Vector3(0,0,-panespeed * Time.deltaTime));
        }
        if(Input.GetKey(KeyCode.W))
        {
            transform.Translate(new Vector3(0,0,panespeed * Time.deltaTime));
        }
        /*
        if(Input.GetKey(KeyCode.RightArrow))
        {
            transform.Rotate(new Vector3(0,rotatespeed*Time.deltaTime,0));
        }
        if(Input.GetKey(KeyCode.LeftArrow))
        {
            transform.Rotate(new Vector3(0,-rotatespeed*Time.deltaTime,0));
        }
        if(Input.GetKey(KeyCode.DownArrow))
        {
            transform.Rotate(new Vector3(-rotatespeed*Time.deltaTime,0,0));
        }
        if(Input.GetKey(KeyCode.UpArrow))
        {
            transform.Rotate(new Vector3(rotatespeed*Time.deltaTime,0,0));
        }*/
        float rotateHorizontal = Input.GetAxis ("Mouse X");
        
        transform.Rotate(transform.up * rotateHorizontal * rotatespeed*1.5f);
        //transform.Rotate(-transform.right * rotateVertical * rotatespeed);
        


    }

    void CheckObjectsInFrustum()
    {
        Vector3 xCam = Camera.main.transform.right;
        Vector3 yCam = Camera.main.transform.up;
        Vector3 zCam = Camera.main.transform.forward;
        
        foreach (GameObject obj in allObjects)
        {
            Vector3 p = obj.transform.position;
            Vector3 c = Camera.main.transform.position;
            Vector3 v = p - c;
            bool isOut = false;

            float proyZ = VecOps.DotProduct(zCam, v);
            if (proyZ < Camera.main.nearClipPlane || proyZ > Camera.main.farClipPlane) isOut = true;
            float distance = VecOps.Magnitude(p - v);
            float frustumHeight = 2.0f * distance * Mathf.Tan(Camera.main.fieldOfView * 0.5f * Mathf.Deg2Rad);
            float frustumWidth = frustumHeight * Camera.main.aspect;

            if (!isOut)
            {
                float proyY = VecOps.DotProduct(yCam, v);
                if (proyY < -frustumHeight / 2.0f || proyY > frustumHeight / 2.0f) isOut = true;
            }
            
            if (!isOut)
            {
                float proyX = VecOps.DotProduct(xCam, v);
                if (proyX < -frustumWidth / 2.0f || proyX > frustumWidth / 2.0f) isOut = true;
            }

            if (!isOut)
            {
                obj.SetActive(true);
                Debug.Log($"{obj.name} is inside the frustum!");
            }
            else
            {
                obj.SetActive(false);
                Debug.Log($"{obj.name} is outside the frustum!");
            }
        }
    }
}
