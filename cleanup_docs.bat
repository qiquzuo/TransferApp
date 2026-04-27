@echo off
chcp 65001 >nul
echo ========================================
echo   文档清理助手
echo ========================================
echo.
echo 以下文档已合并到新文档中，可以安全删除：
echo.
echo 【可删除的旧文档】
echo ----------------------------------------
echo 1.  BUGFIX_v2.1.md
echo 2.  BUILD_GUIDE.md
echo 3.  CHECKLIST.md
echo 4.  DISTRIBUTION.md
echo 5.  DISTRIBUTION_GUIDE.md
echo 6.  DUAL_UI_COMPLETION.md
echo 7.  DUAL_UI_DESIGN.md
echo 8.  ENHANCED_FEATURES.md
echo 9.  FEATURES_v2.2.md
echo 10. INDEX.md
echo 11. MAP.md
echo 12. PROJECT_STRUCTURE.md
echo 13. QUICKSTART.md
echo 14. SUMMARY.md
echo 15. TESTING.md
echo 16. TEST_GUIDE.md
echo 17. TEST_REPORT.md
echo 18. UI_DESIGN.md
echo 19. WELCOME.md
echo 20. AUTO_REFRESH_FEATURE.md
echo 21. AUTO_REFRESH_TEST.md
echo.
echo 【保留的核心文档】
echo ----------------------------------------
echo ✓ README_COMPLETE.md       - 完整使用指南
echo ✓ API_REFERENCE.md         - API参考文档
echo ✓ TROUBLESHOOTING.md       - 故障排查指南
echo ✓ DEVELOPER_GUIDE.md       - 开发者指南
echo ✓ DOCUMENTATION_INDEX.md   - 文档索引（本文）
echo.
echo 【Android文档（在android-app目录）】
echo ✓ RESPONSIVE_ADAPTATION.md
echo ✓ LAYOUT_OPTIMIZATION.md
echo ✓ BUILD_TEST_GUIDE.md
echo ✓ QUICK_START.md
echo.
echo ========================================
echo.
echo 是否删除旧文档？(Y/N)
set /p choice=请输入: 

if /i "%choice%"=="Y" (
    echo.
    echo 正在删除旧文档...
    
    del "BUGFIX_v2.1.md" 2>nul
    del "BUILD_GUIDE.md" 2>nul
    del "CHECKLIST.md" 2>nul
    del "DISTRIBUTION.md" 2>nul
    del "DISTRIBUTION_GUIDE.md" 2>nul
    del "DUAL_UI_COMPLETION.md" 2>nul
    del "DUAL_UI_DESIGN.md" 2>nul
    del "ENHANCED_FEATURES.md" 2>nul
    del "FEATURES_v2.2.md" 2>nul
    del "INDEX.md" 2>nul
    del "MAP.md" 2>nul
    del "PROJECT_STRUCTURE.md" 2>nul
    del "QUICKSTART.md" 2>nul
    del "SUMMARY.md" 2>nul
    del "TESTING.md" 2>nul
    del "TEST_GUIDE.md" 2>nul
    del "TEST_REPORT.md" 2>nul
    del "UI_DESIGN.md" 2>nul
    del "WELCOME.md" 2>nul
    del "AUTO_REFRESH_FEATURE.md" 2>nul
    del "AUTO_REFRESH_TEST.md" 2>nul
    
    echo.
    echo ✅ 旧文档已删除！
    echo.
    echo 保留的核心文档：
    echo   - README_COMPLETE.md
    echo   - API_REFERENCE.md
    echo   - TROUBLESHOOTING.md
    echo   - DEVELOPER_GUIDE.md
    echo   - DOCUMENTATION_INDEX.md
) else (
    echo.
    echo 已取消删除操作。
    echo 你可以稍后手动删除不需要的文档。
)

echo.
echo ========================================
pause
