# Source bottom bar status

This is a navigation-only implementation, not a complete fix for issue 7.

Recovered and bound native Main g_chat/bg_chat/btn_friend, Friend/Friend_Window, Chat/ChatView_MiniWindow and Mail/GameHelp_Window. Assistant labels use GameHelpListConfig resolved source names, and FunctionConfig 135 supplies its icon and level gate. No prototype window layouts are used.

No social or assistant server service is connected. Request/send/start controls are disabled; native fields explicitly say the service is not connected. No fake friends, messages, owned mounts, rewards or purchases are produced. Mount controls remain hidden because no verified ownership adapter exists. This is an unresolved part of issue 7, not proof mounts work.

The original UI assets and client records do not provide an executable server implementation. Implementing or recovering those services is separate from restoring visual assets. Do not call issue 7 solved or this patch a fully working social system.

Issue 6 remains open: user's shop reports Updated shop service is required. User postponed that investigation. Quest tabs remain open pending user's video. Building name presentation, attack effects and creature stat growth remain open. User confirmed face, water and native battle presentation.
