from handler.user import Login, \
                          Logout
from handler.node import Main, \
                          NodeManage, \
                          Top, \
                          LeftGroup, \
                          GroupList, \
                          RightNode, \
                          ConCreate, \
                          ConAction, \
                          ConStart, \
                          ConStop, \
                          ConDestroy, \
                          ConRestart, \
                          ConManage, \
                          ConModify

urls = [
    (r"/",           Login),
    (r"/login",      Login),
    (r"/logout",     Logout),
    (r"/main",       Main),
    (r"/base",       Top),
    (r"/leftgroup",  LeftGroup),
    (r"/grouplist",  GroupList),
    (r"/nodemanage", NodeManage),
    (r"/node",        RightNode),
    (r"/concreate",   ConCreate),
    (r"/conaction",   ConAction),
    (r"/constart",    ConStart),
    (r"/constop",     ConStop),
    (r"/conrestart",  ConRestart),
    (r"/condestroy",  ConDestroy),
    (r"/conmanage",   ConManage),
    (r"/conmodify",    ConModify),
]