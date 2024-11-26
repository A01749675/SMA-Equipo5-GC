using System;
using System.Collections;
using System.Collections.Generic;
using System.ComponentModel.Design;
using UnityEngine;
using UnityEngine.ProBuilder;
using UnityEngine.UIElements;

public class Movement3 : MonoBehaviour
{
    
    public float x;
    public float z;
    ProBuilderMesh pbMesh;
    MeshRenderer pbRenderer;
    List<Vector3> vertices;
    Matrix4x4 pedTranslate;
    Vector3 position;
    Matrix4x4 roty;
    Matrix4x4 pneg;
    Matrix4x4 ppos;
    Vector3 pivot;
    [SerializeField]
    public float angle;
    Matrix4x4 m;
    float objectiveAngle;
    bool flag;
    Matrix4x4 scale;
    public GameObject pedPrefab;
    GameObject pedestrian;
    GameObject ped;
    public Connection con;
    public int id;

    public bool callForNextPos;
    public bool waitingForNextPos;
    public bool started;
    public int i;
    public bool getStarted;
    bool flagrotating;

    Matrix4x4 pedTranslateR;
    bool once;
    Vector3 temp;
    float rotating_angle;
    Matrix4x4 rotyr;
    int rotating_dir;
    bool startFinished;
    public PedController pedController;

    
    
    


    // Start is called before the first frame update
    void Start()
    {
        startFinished = false;
        // Instancia el prefab del coche
        if (pedPrefab != null)
        {
            pedestrian = Instantiate(pedPrefab);
            ped = pedestrian.transform.GetChild(0).gameObject;
        }
        else
        {
            //////DebugLogError("ped prefab is not assigned!");
            return;
        }
        x= 0;
        z = 0;
        pbMesh = ped.GetComponent<ProBuilderMesh>();
        pbRenderer = ped.GetComponent<MeshRenderer>();
        vertices =new List<Vector3>(pbMesh.positions);
        pedTranslate = VecOps.TranslateM(new Vector3 (x, 0, z) );
        position = new Vector3 (x, 0, z);
        roty = VecOps.RotateYM(angle);
        rotyr = VecOps.RotateYM(0);
        //////DebugLog(angle);
        //////DebugLog(roty);
        scale= VecOps.ScaleM(new Vector3 (0.15f,0.15f,0.15f));
        m =  pedTranslate *roty*scale;
        started = false;
        //////DebugLog(m);
        pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
        pbMesh.ToMesh();
        pbMesh.Refresh();
        pivot = new Vector3 (0,0,0);
        ppos = VecOps.TranslateM(pivot);
        pneg = VecOps.TranslateM(-pivot);
        flag = false;
        waitingForNextPos = false;
        callForNextPos = false;
        i = 0;
        getStarted = false;
        once = false;
        startFinished=true;
        
    }

    // Update is called once per frame
    void Update()
    {

        if(!started){
            //Debug.Log("Not started" + id);
            //Debug.Log("getStarted" + getStarted);
            if(getStarted){
                //Debug.Log("BBBBBBBBBBBBBBB");
                ////DebugLog("Receriving positions");
                /*pedTranslate = VecOps.TranslateM(new Vector3 (x+0.5f, 0, z+0.5f) );
                pivot = new Vector3 (0,0,0);
                position = new Vector3 (x, 0, z);
                ////DebugLog("Angulo = " + angle);
                roty = VecOps.RotateYM(angle);
                pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
                pbMesh.ToMesh();
                pbMesh.Refresh();
                ////DebugLog("The position is: "+position);
                ppos = VecOps.TranslateM(pivot);
                pneg = VecOps.TranslateM(-pivot);
                m = scale*pedTranslate *ppos * roty * pneg;
                pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
                pbMesh.ToMesh();
                //////DebugLog(m);
                pbMesh.Refresh();*/
                started = true;
            }
        }
        else{
            Debug.Log("Ya empezó");
            if(AproximadamenteIgual(x,position.x,0.1f) & AproximadamenteIgual(z,position.z,0.1f) ){
                /* Debug.Log("En objetivo " + id);
                Debug.Log("x1" + x);
                Debug.Log("callForNextPos" + callForNextPos);
                Debug.Log("waitingForNextPos" + waitingForNextPos);
                Debug.Log("con.addingPos" + con.addingPos);
                Debug.Log("x2" + x); */
                if (!callForNextPos  && !waitingForNextPos && !con.addingPos){
                    //Debug.Log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
                    //Debug.Log("ped id " + id + " tried to get a new position");
                    flag = false;
                    callForNextPos = true;
                    pedController.trycalling();
                    i +=1;

                //////DebugLog("Llame al servidor" + i);
                }
                //Debug.Log("Autoped " + id + " en posición objetivo y esperando respuesta del servidor");

            } else{
                //Debug.Log("En movimiento");
                if (AproximadamenteIgual(position.x, x, 0.1f)){
                    //////DebugLog("x igual");
                    if (AproximadamenteIgual(angle,-90) || AproximadamenteIgual(angle,90)  || AproximadamenteIgual(angle,270) || AproximadamenteIgual(angle,-270)){
                        //////DebugLog("Avanzaré a z");
                        position.z=m[2,3];
                            if(position.z < z){
                                move_z(0.1f);
                                //////DebugLog("Arriba");
                            } else{
                                move_z(-0.1f);
                                //////DebugLog("Abajo");
                            }
                            flag = false;
                        
                    } else{
                        //////DebugLog("Voy a girar hacia z");
                        if (!flag){
                            
                            if (AproximadamenteIgual(angle,0)){
                                if(z>position.z){
                                    //Check
                                    //Debug.Log("Aqui");
                                    
                                    pivot= new Vector3 (pedTranslate[0,3],position.y,pedTranslate[2,3]+0.5f);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, 0.5f));
                                    temp = new Vector3(0.5f, 0, 0.5f);
                                    objectiveAngle = -90;
                                } else {
                                    //Check
                                    pivot= new Vector3 (pedTranslate[0,3],position.y,pedTranslate[2,3]-0.5f);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, -0.5f));
                                    temp = new Vector3(0.5f, 0, -0.5f);
                                    objectiveAngle = 90;
                                }
                            } else if (AproximadamenteIgual(angle,180)){
                                if(z>position.z){
                                    //Check
                                    
                                    pivot= new Vector3 (pedTranslate[0,3],position.y,pedTranslate[2,3]+0.5f);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, 0.5f));
                                    temp = new Vector3(-0.5f, 0, 0.5f);
                                    objectiveAngle = 270;
                                } else {
                                    //Check
                                    
                                    pivot= new Vector3 (pedTranslate[0,3],position.y,pedTranslate[2,3]-0.5f);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, -0.5f));
                                    temp = new Vector3(-0.5f, 0, -0.5f);
                                    objectiveAngle = 90;
                                }
                            } else{
                                if (z>position.z){
                                    //Check
                                    
                                    pivot= new Vector3 (pedTranslate[0,3],position.y,pedTranslate[2,3]+0.5f);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0f, 0,2f));*/
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, 0.5f));
                                    temp= new Vector3(-0.5f, 0, 0.5f);
                                    objectiveAngle = -90;
                                } else {
                                    //Check // Se presento buuug
                                    pivot= new Vector3 (pedTranslate[0,3],position.y,pedTranslate[2,3]-0.5f);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, -0.5f));
                                    temp = new Vector3(-0.5f, 0, -0.5f);
                                    objectiveAngle = -270;
                                }
                            }
                            flag = true;
                            flagrotating = true;
                        } else{
                            if (angle > objectiveAngle){
                                rotate_left();
                                //////DebugLog("LEEEEEEEEEFT 1");
                            } else if(angle<objectiveAngle){
                                rotate_right();
                                //////DebugLog("RIIIIIIIIGHT 1");
                            }
                            if (AproximadamenteIgual(angle,objectiveAngle,3)){
                                angle = objectiveAngle;
                            }
                            ////DebugLog("Rotar a " + objectiveAngle);
                            //roty=VecOps.RotateYM(objectiveAngle);
                            //angle = objectiveAngle;
                        }
                    }
                } else{
                    //////DebugLog("x diferente");
                    if (AproximadamenteIgual(angle, 0) || AproximadamenteIgual(angle,180) || AproximadamenteIgual(angle,-180) || AproximadamenteIgual(angle,360) || AproximadamenteIgual(angle,-360)){
                    position.x=m[0,3];
                    //////DebugLog("Estoy apuntando hacia x");
                        if(position.x < x){
                            move_x(0.1f);
                            //////DebugLog("Derecha");
                        } else{
                            move_x(-0.1f);
                            //////DebugLog("Izquierda");
                        }
                        if (AproximadamenteIgual(angle,360) || AproximadamenteIgual(angle,-360)){
                            angle = 0;
                        }
                        flag = false;
                    } else{
                        //////DebugLog("Voy a girar hacia x");
                        //////DebugLog(flag);
                        if (!flag){ 
                            if (AproximadamenteIgual(angle,-90)){
                                if(x>position.x){
                                    //Check
                                    pivot= new Vector3 (pedTranslate[0,3]+0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(1f, 0,1f));
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, 0.5f));
                                    temp = new Vector3(0.5f, 0, 0.5f);
                                    objectiveAngle = 0;
                                    
                                } else {
                                    //Check
                                    
                                    pivot= new Vector3 (pedTranslate[0,3]-0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, 0.5f));
                                    temp = new Vector3(-0.5f, 0, 0.5f);
                                    objectiveAngle = -180;
                                }
                            } else if (AproximadamenteIgual(angle,-270)){
                                if(x>position.x){
                                    //Check
                                
                                    pivot= new Vector3 (pedTranslate[0,3]+0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, -0.5f));
                                    temp = new Vector3(0.5f, 0, -0.5f);
                                    objectiveAngle = -360;
                                } else {
                                    //Check
                                
                                    pivot= new Vector3 (pedTranslate[0,3]-0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, -0.5f));
                                    temp = new Vector3(-0.5f, 0, -0.5f);
                                    objectiveAngle = -180;
                                }
                            } else if (AproximadamenteIgual(angle,90)){
                                if(x>position.x){
                                    // Check
                                    
                                    pivot= new Vector3 (pedTranslate[0,3]+0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(1f, 0, -1f));
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, -0.5f));
                                    temp = new Vector3(0.5f, 0, -0.5f);
                                    objectiveAngle = 0;
                                } else {
                                    //Check
                                    pivot= new Vector3 (pedTranslate[0,3]-0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(1f, 0, -1f));
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, -1f));
                                    temp = new Vector3(-0.5f, 0, -0.5f);
                                    objectiveAngle = 180;
                                }
                            } else if (AproximadamenteIgual(angle,270)){
                                if(x>position.x){
                                    //Check
                                    pivot= new Vector3 (pedTranslate[0,3]+0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(0.5f, 0, -0.5f));
                                    temp = new Vector3(0.5f, 0, 0.5f);
                                    objectiveAngle = 360;
                                } else {
                                    //Check
                                    pivot= new Vector3 (pedTranslate[0,3]-0.5f,position.y,pedTranslate[2,3]);
                                    //pedTranslate *= VecOps.TranslateM(new Vector3(-0.5f, 0, 0.5f));
                                    temp = new Vector3(-0.5f, 0, 0.5f);
                                    objectiveAngle = 180;
                                }
                            }
                            flag = true;
                            flagrotating = true;
                        } else{
                            /*if (objectiveAngle != 0 && objectiveAngle != 180 && objectiveAngle != -180 && objectiveAngle != 360 && objectiveAngle != -360){
                                flag = false;
                            }*/
                            if (angle > objectiveAngle){ 
                                rotate_left();
                                //////DebugLog("LEEEEEEEEEFT 2");
                            } else if(angle<objectiveAngle){
                                rotate_right();
                                //////DebugLog("RIIIIIIIIGHT 2");
                            }
                            ////DebugLog("Rotar a " + objectiveAngle);
                            //roty=VecOps.RotateYM(objectiveAngle);
                            //angle = objectiveAngle;
                            if (AproximadamenteIgual(angle,objectiveAngle,3)){
                                angle = objectiveAngle;
                            }
                            
                        }
                    }
                }
            }
            ppos = VecOps.TranslateM(pivot);
            pneg = VecOps.TranslateM(-pivot);
            
            
            m =   pedTranslate *roty*scale;
            pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
            pbMesh.ToMesh();
            pbMesh.Refresh();
            //m = scale*pedTranslate *ppos * roty * pneg;


            
            if(angle == objectiveAngle){
                flag = false;
            }
        }
    }
    void move_x(float speed)
    {
        position.x += speed;
        pedTranslate *= VecOps.TranslateM(new Vector3(speed, 0, 0));
    }

    void move_z(float speed)
    {
        position.z += speed;
        pedTranslate *= VecOps.TranslateM(new Vector3(0, 0, speed));
    }

    void rotate_left()
    {
        angle-=4;
        roty *= VecOps.RotateYM(-4); // Rotación acumulativa
    }

    void rotate_right()
    {
        angle+=4;
        roty *= VecOps.RotateYM(4); // Rotación acumulativa
    }

    bool AproximadamenteIgual(float valor1, float valor2, float tolerancia = 0.001f)
    {
        return Mathf.Abs(valor1 - valor2) < tolerancia;
    }

    /*void rotate_leftr()
    {
        rotating_angle-=4;
        rotyr *= VecOps.RotateYM(-4); // Rotación acumulativa
    }

    void rotate_rightr()
    {
        rotating_angle+=4;
        rotyr *= VecOps.RotateYM(4); // Rotación acumulativa
    }

    void rotating(){
        if (!once){
            ////Debug.Log("Guardando pedTranslateR");
            pedTranslateR = pedTranslate;
            ////Debug.Log(pedTranslateR);
            once = true;
            rotating_angle = 0;
            if (angle > objectiveAngle){
                rotating_dir =-1;
            } else if(angle < objectiveAngle){
                rotating_dir = 1;
            }
            //Debug.Log("Iniciando en" +m[0,3]);
            rotyr = VecOps.RotateYM(0);
        }
        if (rotating_dir == -1){
            ////Debug.Log("Rotando a la izquierda");
            //rotate_left();
            rotate_leftr();
            
        } else if(rotating_dir == 1){
            ////Debug.Log("Rotando a la derecha");
            //rotate_right();
            rotate_rightr();
        }
        
        pneg = VecOps.TranslateM(-pivot);
        ppos = VecOps.TranslateM(pivot);
        ////Debug.Log(pivot);
        m =  ppos * rotyr * pneg * pedTranslateR* roty* scale;
        ////Debug.Log(m[0,3]);
        //GameObject pivote = GameObject.CreatePrimitive(PrimitiveType.Sphere);
        //pivote.transform.position = pivot;
        pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
        pbMesh.ToMesh();
        pbMesh.Refresh();

        if (AproximadamenteIgual(rotating_angle, 90,3) || AproximadamenteIgual(rotating_angle, -90, 3) || AproximadamenteIgual(rotating_angle, 0, 3) || AproximadamenteIgual(rotating_angle,180,3) || AproximadamenteIgual(rotating_angle, -180,3) || AproximadamenteIgual(rotating_angle, 270,3) || AproximadamenteIgual(rotating_angle,-270,3) || AproximadamenteIgual(rotating_angle,360,3) || AproximadamenteIgual(rotating_angle, -360, 3)) {
            flagrotating = false;
            once = false;
            pedTranslate *= VecOps.TranslateM(temp); 
            if (rotating_dir == 1){
                angle+=90;
                roty = VecOps.RotateYM(angle);
            } else if(rotating_dir == -1){
                angle-=90;
                roty = VecOps.RotateYM(angle);
            }
        }

    }*/

public void setX(float x_n){
    if((int)x == (int)x_n){
        return;
    } else{
        if(x > x_n){
            x = x_n+0.1f;
        } else{
            x = x_n+0.9f;
        }
    }
}

public void setZ(float z_n){
    if((int)z == (int)z_n){
        return;
    } else{
        if(z > z_n){
            z = z_n+0.1f;
        } else{
            z = z_n+0.9f;
        }
    }
}
public void setAngle(string direction){
    if(!started){
        ////DebugLog("Seteando angulo");
        ////DebugLog(direction);
        
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
                ////DebugLogWarning("Dirección no reconocida: " + direction);
                break;
        }
    }
}
public void setInitialPos(float x_n, float z_n, string direction)
{
    StartCoroutine(SetInitialPosCoroutine(x_n, z_n, direction));
}

private IEnumerator SetInitialPosCoroutine(float x_n, float z_n, string direction)
{
    // Espera hasta que Start haya terminado
    while (!startFinished)
    {
        yield return null;
    }

    //Debug.Log("Setting initial position for ped " + id + " to (" + x_n + ", " + z_n + ")");
    pedTranslate = VecOps.TranslateM(new Vector3 (x_n+0.5f, 0, z_n+0.5f) );
    pivot = new Vector3 (0,0,0);
    position = new Vector3 (x_n, 0, z_n);
    ////DebugLog("Angulo = " + angle);
    roty = VecOps.RotateYM(angle);
    pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
    pbMesh.ToMesh();
    pbMesh.Refresh();
    ////DebugLog("The position is: "+position);
    ppos = VecOps.TranslateM(pivot);
    pneg = VecOps.TranslateM(-pivot);
    m = pedTranslate *ppos * roty * pneg* scale;
    pbMesh.positions = VecOps.ApplyTransform(vertices, m).ToArray();
    pbMesh.ToMesh();
    pbMesh.Refresh();
    pbRenderer.enabled = true;
    x=x_n;
    z=z_n;
    position = new Vector3 (x, 0, z);
    getStarted = true;
}
public void setArrived(){
    //Debug.Log("Llegué");
    ped.SetActive(false);

}
}

