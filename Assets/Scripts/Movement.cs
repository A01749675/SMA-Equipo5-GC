using System;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.ProBuilder;
using UnityEngine.UIElements;

public class Movement : MonoBehaviour
{
    
    public float x;
    public float z;
    ProBuilderMesh pbMesh;
    List<Vector3> vertices;
    Matrix4x4 carTranslate;
    Vector3 position;
    Matrix4x4 roty;
    Matrix4x4 pneg;
    Matrix4x4 ppos;
    Vector3 pivot;
    [SerializeField]
    float angle;
    Matrix4x4 m;
    float objectiveAngle;
    bool flag;
    Matrix4x4 scale;
    [SerializeField]
    GameObject carPrefab;
    GameObject car;
    [SerializeField]
    Connection con;

    public bool callForNextPos;
    public bool waitingForNextPos;
    public bool started;
    public int i;

    
    
    


    // Start is called before the first frame update
    void Start()
    {
        // Instancia el prefab del coche
        if (carPrefab != null)
        {
            car = Instantiate(carPrefab);
            car.name = "CarPrueba";
        }
        else
        {
            //Debug.LogError("Car prefab is not assigned!");
            return;
        }
        x= 0;
        z = 0;
        pbMesh = car.GetComponent<ProBuilderMesh>();
        vertices =new List<Vector3>(pbMesh.positions);
        carTranslate = VecOps.TranslateM(new Vector3 (x, 0, z) );
        position = new Vector3 (x, 0, z);
        roty = VecOps.RotateYM(angle);
        //Debug.Log(angle);
        //Debug.Log(roty);
        scale= VecOps.ScaleM(new Vector3 (1,1,1));
        m =  scale*carTranslate *roty;
        started = false;
        //Debug.Log(m);
        pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
        pbMesh.ToMesh();
        pbMesh.Refresh();
        pivot = new Vector3 (0,0,0);
        ppos = VecOps.TranslateM(pivot);
        pneg = VecOps.TranslateM(-pivot);
        flag = false;
        waitingForNextPos = false;
        callForNextPos = true;
        i = 0;
        
    }

    // Update is called once per frame
    void Update()
    {

        if(!started){
            Debug.Log("Not started");
            if(!callForNextPos && !con.addingPos){
                Debug.Log("Receriving positions");
                carTranslate = VecOps.TranslateM(new Vector3 (x, 0, z) );
                pivot = new Vector3 (0,0,0);
                position = new Vector3 (x, 0, z);
                Debug.Log("Angulo = " + angle);
                roty = VecOps.RotateYM(angle);
                pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
                pbMesh.ToMesh();
                pbMesh.Refresh();
                Debug.Log("The position is: "+position);
                ppos = VecOps.TranslateM(pivot);
                pneg = VecOps.TranslateM(-pivot);
                m = scale*carTranslate *ppos * roty * pneg;
                pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
                pbMesh.ToMesh();
                //Debug.Log(m);
                pbMesh.Refresh();
                started = true;
            }
        }
        else{

            if(AproximadamenteIgual(x,position.x,0.1f) & AproximadamenteIgual(z,position.z,0.1f)){
                if (!callForNextPos  && !waitingForNextPos){
                Debug.Log("En objetivo");
                flag = false;
                callForNextPos = true;
                //con.CallNextPos();
                i +=1;
                Debug.Log("Llame al servidor" + i);
                }

            } else{
                if (AproximadamenteIgual(position.x, x, 0.1f)){
                    //Debug.Log("x igual");
                    if (AproximadamenteIgual(angle,-90) || AproximadamenteIgual(angle,90)  || AproximadamenteIgual(angle,270) || AproximadamenteIgual(angle,-270)){
                        //Debug.Log("Avanzaré a z");
                        position.z=m[2,3];
                            if(position.z < z){
                                move_z(0.1f);
                                //Debug.Log("Arriba");
                            } else{
                                move_z(-0.1f);
                                //Debug.Log("Abajo");
                            }
                            flag = false;
                        
                    } else{
                        //Debug.Log("Voy a girar hacia z");
                        if (!flag){
                            
                            if (AproximadamenteIgual(angle,0)){
                                if(z>position.z){
                                    //Check
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    
                                    objectiveAngle = -90;
                                } else {
                                    //Check
                                    pivot= new Vector3 (0,position.y,-0.5f);
                                    objectiveAngle = 90;
                                }
                            } else if (AproximadamenteIgual(angle,180)){
                                if(z>position.z){
                                    //Check
                                    
                                    pivot= new Vector3 (0,position.y,-0.5f);
                                    objectiveAngle = 270;
                                } else {
                                    //Check
                                    
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    objectiveAngle = 90;
                                }
                            } else{
                                if (z>position.z){
                                    //Check
                                    
                                    pivot= new Vector3 (0,position.y,-0.5f);
                                    //carTranslate *= VecOps.TranslateM(new Vector3(0f, 0,2f));*/
                                    objectiveAngle = -90;
                                } else {
                                    //Check // Se presento buuug
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    objectiveAngle = -270;
                                }
                            }
                            flag = true;
                        } else{
                            if (angle > objectiveAngle){
                                rotate_left();
                                //Debug.Log("LEEEEEEEEEFT 1");
                            } else if(angle<objectiveAngle){
                                rotate_right();
                                //Debug.Log("RIIIIIIIIGHT 1");
                            }
                        }
                    }
                } else{
                    //Debug.Log("x diferente");
                    if (AproximadamenteIgual(angle, 0) || AproximadamenteIgual(angle,180) || AproximadamenteIgual(angle,-180) || AproximadamenteIgual(angle,360) || AproximadamenteIgual(angle,-360)){
                    position.x=m[0,3];
                    //Debug.Log("Estoy apuntando hacia x");
                        if(position.x < x){
                            move_x(0.1f);
                            //Debug.Log("Derecha");
                        } else{
                            move_x(-0.1f);
                            //Debug.Log("Izquierda");
                        }
                        if (AproximadamenteIgual(angle,360) || AproximadamenteIgual(angle,-360)){
                            angle = 0;
                        }
                        flag = false;
                    } else{
                        //Debug.Log("Voy a girar hacia x");
                        //Debug.Log(flag);
                        if (!flag){ 

                            if (AproximadamenteIgual(angle,-90)){
                                if(x>position.x){
                                    //Check
                                    pivot= new Vector3 (0,position.y,-0.5f);
                                    //carTranslate *= VecOps.TranslateM(new Vector3(1f, 0,1f));*/
                                    objectiveAngle = 0;
                                } else {
                                    //Check
                                    
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    objectiveAngle = -180;
                                }
                            } else if (AproximadamenteIgual(angle,-270)){
                                if(x>position.x){
                                    //Check
                                
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    objectiveAngle = -360;
                                } else {
                                    //Check
                                
                                    pivot= new Vector3 (0,position.y,-0.5f);
                                    
                                    objectiveAngle = -180;
                                }
                            } else if (AproximadamenteIgual(angle,90)){
                                if(x>position.x){
                                    // Check
                                    
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    //carTranslate *= VecOps.TranslateM(new Vector3(1f, 0, -1f));*/
                                    objectiveAngle = 0;
                                } else {
                                    //Check
                                    pivot= new Vector3 (0,position.y,-0.5f);
                                    //carTranslate *= VecOps.TranslateM(new Vector3(1f, 0, -1f));*/
                                    objectiveAngle = 180;
                                }
                            } else if (AproximadamenteIgual(angle,270)){
                                if(x>position.x){
                                    //Check
                                    pivot= new Vector3 (-0f,position.y,-0.5f);
                                    objectiveAngle = 360;
                                } else {
                                    //Check
                                    pivot= new Vector3 (0,position.y,0.5f);
                                    carTranslate *= VecOps.TranslateM(new Vector3(-1f, 0, -1f));
                                    objectiveAngle = 180;
                                }
                            }
                            flag = true;
                        } else{
                            /*if (objectiveAngle != 0 && objectiveAngle != 180 && objectiveAngle != -180 && objectiveAngle != 360 && objectiveAngle != -360){
                                flag = false;
                            }*/
                            if (angle > objectiveAngle){ 
                                rotate_left();
                                //Debug.Log("LEEEEEEEEEFT 2");
                            } else if(angle<objectiveAngle){
                                rotate_right();
                                //Debug.Log("RIIIIIIIIGHT 2");
                            }
                        }
                    }
                }
            }
            ppos = VecOps.TranslateM(pivot);
            pneg = VecOps.TranslateM(-pivot);
            
            m = scale*carTranslate *ppos * roty * pneg;

            if (!AproximadamenteIgual(m[0,3], position.x, 0.6f)){
                Debug.Log("Se tepeo en x");
            }
            if (!AproximadamenteIgual(m[2,3], position.z, 0.6f)){
                Debug.Log("Se tepeo en z");
            }

            pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
            pbMesh.ToMesh();
            //Debug.Log(m);
            pbMesh.Refresh();
            if(angle == objectiveAngle){
                flag = false;
            }
        }
    }
    void move_x(float speed)
{
    position.x += speed;
    carTranslate *= VecOps.TranslateM(new Vector3(speed, 0, 0));
}

void move_z(float speed)
{
    position.z += speed;
    carTranslate *= VecOps.TranslateM(new Vector3(0, 0, speed));
}

void rotate_left()
{
    angle--;
    roty *= VecOps.RotateYM(-1); // Rotación acumulativa
}

void rotate_right()
{
    angle++;
    roty *= VecOps.RotateYM(1); // Rotación acumulativa
}

bool AproximadamenteIgual(float valor1, float valor2, float tolerancia = 0.001f)
{
    return Mathf.Abs(valor1 - valor2) < tolerancia;
}

public void setX(float x_n){
    if (x == x_n){
        x = x_n;
        return;
    }
    if(x > x_n){
        x = x_n+1;
    } else{
        x = x_n;
    }
}

public void setZ(float z_n){
    if (z == z_n){
        z = z_n;
        return;
    }
    if(z > z_n){
        z = z_n+1;
    } else{
        z = z_n;
    }
}
public void setAngle(string direction){
    if(!started){
        Debug.Log("Seteando angulo");
        Debug.Log(direction);
        
        switch (direction)
        {
            case "N":
                angle = 270;
                break;
            case "E":
                angle = 0;
                break;
            case "S":
                angle = 90;
                break;
            case "W":
                angle = 180;
                break;
            default:
                Debug.LogWarning("Dirección no reconocida: " + direction);
                break;
        }
    }
}
}

