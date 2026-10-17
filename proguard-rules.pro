# JavaScript ブリッジのメソッドを難読化から除外
-keepclassmembers class jp.ashenroads.app.MainActivity$AndroidBridge {
    public *;
}
